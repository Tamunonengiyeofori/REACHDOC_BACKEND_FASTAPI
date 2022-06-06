#THIS IS THE MAIN FASTAPI PROGRAM FILE THAT CALLS ALL OTHER FILE PACKAGES

# import fastapi
from fastapi import FastAPI
#SQLALCHEMY DEPENDENCIES FOR ORM and Pydantic Schema models
from . import models
from .database import engine
#the path operations for patient and user from routers.py
from .routers import patient, admin, auth, doctor

#Create all the ORM models in the database 
# models.Base.metadata.create_all(bind=engine)

# create an instance of the fastapi class
app = FastAPI()
           
#create welcome path operation
@app.get("/")
def root():
    return{"Message":"Welcome to the ReachDoc API"}

# ADD the path operations from routers.py to the FastAPI app instance so it will reference them and import them.
app.include_router(patient.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(doctor.router)
