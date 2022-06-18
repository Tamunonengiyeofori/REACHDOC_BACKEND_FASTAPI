#THIS FILE HANDLES ALL PATH OPERATIONS FOR PATIENTS

from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from typing import List, Optional
#SQLALCHEMY DEPENDENCIES FOR ORM and Pydantic Schema models 
from .. import schemas, models, Oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..rolechecker import RoleChecker

#create a router object from the APIRouter class
router = APIRouter(
    prefix="/patients",
    tags = ["Patients"]
)

# create an instance of the RoleChecker class
#Role based access control for patients
#check if active user is an admin and grant user access to CRUD operations for patients
allow_create_patient = RoleChecker(["admin"])
allow_update_patient = RoleChecker(["patient", "admin"])
allow_delete_patient = RoleChecker(["admin"])
allow_get_patients = RoleChecker(["admin"])

#create path operation to get all patients
@router.get("/", response_model=List[schemas.PatientResponse], dependencies=[Depends(allow_get_patients)])
def get_patients(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user), 
                 limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    patients = db.query(models.Patient).all()
    print(current_user.role)
    return patients

#create path operation to get patient by id 
@router.get("/{id}", response_model=schemas.PatientResponse, dependencies=[Depends(allow_get_patients)])
def get_patient(id: int , db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    patient = db.query(models.Patient).filter(models.Patient.id == id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"patient with id: {id} does not exist")
    return patient  


#Create a path operation for creating a patient
@router.post("/" , response_model=schemas.PatientResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(allow_create_patient)])
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    print(current_user.id)
    new_patient = models.Patient(creator_id=current_user.id, **patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


#Create a path operation for updating a patient
@router.put("/{id}", response_model=schemas.PatientResponse, dependencies=[Depends(allow_update_patient)])
def update_patient(id: int, updated_patient: schemas.PatientCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    patient_query = db.query(models.Patient).filter(models.Patient.id == id)
    patient = patient_query.first()
    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The patient with id: {id} was not found")
    patient_query.update(updated_patient.dict() , synchronize_session=False)
    #save changes to database
    db.commit()
    return patient_query.first() 

#Create a path operation for deleting a patient
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allow_delete_patient)])
def delete_patient(id: int, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    patient = db.query(models.Patient).filter(models.Patient.id == id)
    deleted_patient = patient.first()
    if deleted_patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                           detail=f"The patient wilth id: {id} was not found")
    patient.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)