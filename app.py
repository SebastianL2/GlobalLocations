from routes import zipcodes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from config import db


# create FastAPI instance
app = FastAPI()

origins = ["*"]
# middleware to allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(zipcodes.router)


@app.on_event("startup")
def startup_db_client():
    try:
        db.conn.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


@app.on_event("shutdown")
def shutdown_db_client():
    db.conn.close()


@app.get("/")
def read_root():
    return {"message": "Bienvenido al API de Zipcodes"}
