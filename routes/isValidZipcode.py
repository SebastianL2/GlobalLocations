import spacy
from spacy.matcher import Matcher
from .countries import countries_dict

nlp = spacy.load("en_core_web_sm")


def is_valid_postal_code(zipcode: str):

    matcher = Matcher(nlp.vocab)

    digit, letter, alpha = contar_caracteres(zipcode)
    print("Tiene {} letras, {} digitos y {} caracteres.".format(letter, digit, alpha))

    patterns = {
        # Codigo postal de ESTADOS UNIDOS
        "ZIPCODE_US": [{"SHAPE": "dddd"}, {"ORTH": "-"}, {"SHAPE": "ddddd"}],
        # Codigo postal de CANADA
        "ZIPCODE_CA": [
            {"SHAPE": "XdX"},
            {"IS_SPACE": True, "OP": "?"},
            {"SHAPE": "dXd"},
        ],
        # Codigo postal de COLOMBIA, Belarus,
        "ZIPCODE_CO": [{"SHAPE": "dddddd"}],
        # Codigo postal de AUSTRALIA, AFGANISTAN, Albania, Armenia, Argentina, Austria, Bangladesh, Belgica
        "ZIPCODE_AU": [{"SHAPE": "dddd"}],
        # Codigo postal de ESPAÑA, Aland Islands, Algeria, Bhutan
        "ZIPCODE_ES": [{"SHAPE": "ddddd"}],
        "ZIPCODE_GR": [
            {"SHAPE": "ddd"},
            {"IS_SPACE": True, "OP": "?"},
            {"SHAPE": "dd"}
        ],  # Codigo postal de GRECIA
        "ZIPCODE_UK_ONE": [
            {"SHAPE": "XXd"},
            {"IS_SPACE": True, "OP": "?"},
            {"SHAPE": "dXX"}
        ],
        "ZIPCODE_UK_TWO": [
            {"SHAPE": "XXdd"},
            {"IS_SPACE": True, "OP": "?"},
            {"SHAPE": "dXX"}
        ],
        "ZIPCODE_IRLANDA": [{"SHAPE": "Xdd"}],  # Codigo postal de IRLANDA
        "ZIPCODE_AD": [{"SHAPE": "XXddd"}],  # Codigo postal de ANDORRA
        "ZIPCODE_AZ": [{"SHAPE": "XXdddd"}],  # Codigo postal de Azerbaijan
        # Codigo postal de ANGUILA
        "ZIPCODE_AI": [{"SHAPE": "XX-dddd"}],
        # Codigo postal de Argentina
        "ZIPCODE_AR_ONE": [{"SHAPE": "XddddXXX"}],
        "ZIPCODE_AR_TWO": [{"SHAPE": "Xdddd"}],  # Codigo postal de Argentina
        "ZIPCODE_BB": [{"SHAPE": "XXddddd"}],  # Codigo postal de Barbados
        "ZIPCODE_BM_ONE": [
            {"SHAPE": "XX"},
            {"IS_SPACE": True, "OP": "?"},
            {"SHAPE": "dd"}
        ],  # Codigo postal de Bermuda
        "ZIPCODE_BM_TWO": [
            {"SHAPE": "XX"},
            {"IS_SPACE": True, "OP": "?"},
            {"SHAPE": "XX"}
        ],  # Codigo postal de Bermuda
        "ZIPCODE_BR": [{"SHAPE": "ddddd-ddd"}],  # Brazil
        "ZIPCODE_IO": [
            {"SHAPE": "XXdX"},
            {"IS_SPACE": True, "OP": "?"},
            {"SHAPE": "XX"}
        ],  # British Indian Ocean Territory
    }

    for name, pattern in patterns.items():
        matcher.add(name, [pattern])

    doc = nlp(zipcode)

    # verificar_codigo_postal(zipcode, patterns)

    matches = matcher(doc)

    country_possible = []
    for match_id, start, end in matches:
        print(start, end)
        codigo_postal = doc[start:end]
        match_name = nlp.vocab.strings[match_id]
        country_possible.append(match_name)
        print(f"{match_name}: {codigo_postal.text}")

    print(matches)

    if len(matches) == 0:
        return {
            "message": "El código postal no es válido",
            "valid": False,
            "countries": country_possible,
            "data": {
                "letters": letter,
                "digits": digit,
                "characters": alpha,
                "pattern": countries_dict.get((digit, letter, alpha), [])
            }
        }

    return {
        "message": "Código postal válido",
        "valid": True,
        "countries": country_possible,
        "data": {
            "letters": letter,
            "digits": digit,
            "characters": alpha,
            "pattern": countries_dict.get((digit, letter, alpha), [])
        }
    }


def verificar_codigo_postal(texto, patterns):
    doc = nlp(texto)
    for pattern_name, pattern in patterns.items():
        for i, token in enumerate(doc):
            token_match = True
            for j, cond in enumerate(pattern):
                if i + j < len(doc):
                    token_to_check = doc[i + j]
                    if "SHAPE" in cond and token_to_check.shape_ != cond["SHAPE"]:
                        token_match = False
                        break
                    if "ORTH" in cond and token_to_check.text != cond["ORTH"]:
                        token_match = False
                        break
                    if "IS_SPACE" in cond and token_to_check.is_space != cond["IS_SPACE"]:
                        token_match = False
                        break
                else:
                    token_match = False
                    break

            if token_match:
                print(f"El texto coincide con el patrón: {pattern_name}")
                return True

        if not token_match:
            print(
                f"Fallo en la comprobación del patrón {pattern_name} en el token {i + j}: {doc[i + j].text} (condición: {cond})")

    print("No se encontró ningún patrón coincidente.")
    return False


def contar_caracteres(texto):
    letras = 0
    digitos = 0
    caracteres = 0
    for caracter in texto:
        if caracter.isalpha():
            letras += 1
        elif caracter.isdigit():
            digitos += 1
        else:
            caracteres += 1
    return digitos, letras, caracteres
