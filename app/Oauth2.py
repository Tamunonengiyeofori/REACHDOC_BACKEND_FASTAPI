#THIS FILE HANDLES JWT TOKEN CREATION, VALIDATION AND RETRIEVING CURRENT USER SESSION/LOGGED-IN USER.

from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="adminlogin") #TokenUrl is the endpoint for user login
oauth2_scheme_doctor = OAuth2PasswordBearer(tokenUrl="doctorlogin")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# CREATE ACCESS TOKEN USING JWT TOKEN
def create_access_token(data: dict):
    to_encode = data.copy() # create a copy of the data dictionary parameter for jwt payload
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expires}) # update payload with expiry time
    #Create Jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# VERIFY ACCESS TOKEN FOR ADMIN
def verify_access_token_admin(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("admin_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data

# GET THE CURRENT ADMIN USER
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token_admin(token, credentials_exception)
    user = db.query(models.Admin).filter(models.Admin.id == token.id).first()
    return user
    
# VERIFY ACCESS TOKEN FOR DOCTOR       
def verify_access_token_doctor(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("doctor_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data
        
# GET THE CURRENT DOCTOR USER
def get_current_doctor(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token_doctor(token, credentials_exception)
    doctor = db.query(models.Doctor).filter(models.Admin.id == token.id).first()
    return doctor
    