#THIS FILE HANDLES USER LOGIN PATH OPERATION AND AUTHENTICATION 
 
from fastapi import FastAPI,  status, HTTPException, Response, Depends, APIRouter 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, Oauth2 

router = APIRouter(
    tags=["Authentication"]
)

#Create path operation for admin login
@router.post("/adminlogin")
def login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.email == admin_credentials.username).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
        
    if not utils.verify_password(admin_credentials.password , admin.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    #create access token
    access_token = Oauth2.create_access_token(data = {"admin_id": admin.id})
    return {
        "access_token": access_token,
        "token_type":"bearer"
    }
    
#Create path operation for doctor login
@router.post("/doctorlogin")
def login(doctor_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    doctor = db.query(models.Doctor).filter(models.Doctor.email == doctor_credentials.username).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
        
    if not utils.verify_password(doctor_credentials.password, doctor.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
        
    #create access token
    doctor_access_token = Oauth2.create_access_token(data = {"doctor_id": doctor.id})
    return {
        "access_token": doctor_access_token,
        "token_type":"bearer"
    }