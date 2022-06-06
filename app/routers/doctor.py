#THIS FILE HANDLES ALL PATH OPERATIONS FOR DOCTORS

from fastapi import FastAPI, HTTPException, status, Depends, Response, APIRouter
from typing import List, Optional
#SQLALCHEMY DEPENDENCIES FOR ORM and Pydantic Schema models 
from .. import schemas, models, Oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..rolechecker import RoleChecker

#create a router object from the APIRouter class
router = APIRouter(
    prefix="/doctors",
    tags = ["Doctors"]
)

# create an instance of the RoleChecker class
#Role based access control for patients
#check if active user is an admin and grant user access to CRUD operations for patients
allow_create_doctor = RoleChecker(["admin"])
allow_update_doctor = RoleChecker(["doctor", "admin"])
allow_delete_doctor = RoleChecker(["admin"])
allow_get_doctor = RoleChecker(["admin"])

#create path operation to get all doctors
@router.get("/", response_model=List[schemas.DoctorResponse], dependencies=[Depends(allow_get_doctor)])
def get_doctors(db: Session = Depends(get_db), current_admin: int = Depends(Oauth2.get_current_user), 
                 limit: int = 5, skip: int = 0, search: Optional[str] = ""):
    doctor = db.query(models.Doctor).all()
    print(current_admin.role)
    return doctor

#create path operation to get doctor by id 
@router.get("/{id}", response_model=schemas.DoctorResponse, dependencies=[Depends(allow_get_doctor)])
def get_doctor(id: int , db: Session = Depends(get_db), current_admin: int = Depends(Oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"doctor with id: {id} does not exist")
    return doctor


#Create a path operation for creating a doctor
@router.post("/" , response_model=schemas.DoctorResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(allow_create_doctor)])
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db), current_admin: int = Depends(Oauth2.get_current_user)):
    print(current_admin.name)
    new_doctor = models.Doctor(creator_id=current_admin.id, **doctor.dict())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor


#Create a path operation for updating a doctor
@router.put("/{id}", response_model=schemas.DoctorResponse, dependencies=[Depends(allow_update_doctor)])
def update_doctor(id: int, updated_doctor: schemas.DoctorCreate, db: Session = Depends(get_db), current_admin: int = Depends(Oauth2.get_current_user)):
    doctor_query = db.query(models.Doctor).filter(models.Doctor.id == id)
    doctor = doctor_query.first()
    if doctor == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The doctor with id: {id} was not found")
    doctor_query.update(updated_doctor.dict() , synchronize_session=False)
    #save changes to database
    db.commit()
    return doctor_query.first() 

#Create a path operation for deleting a doctor
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allow_delete_doctor)])
def delete_doctor(id: int, db: Session = Depends(get_db), current_admin: int = Depends(Oauth2.get_current_user)):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == id)
    deleted_doctor = doctor.first()
    if deleted_doctor == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                           detail=f"The doctor wilth id: {id} was not found")
    doctor.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)