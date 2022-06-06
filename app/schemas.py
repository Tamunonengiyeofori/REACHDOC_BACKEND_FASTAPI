#THIS FILE HANDLES VALIDATION OF USER HTTP REQUESTS, VALIDATION OF API RESPONSES, VALIDATION OF USER TOKEN AND VALIDATION OF USER TOKEN DATA FOR USER LOGIN USING PYDANTIC SCHEMA MODELS

#PYDANTIC SCHEMA
from pydantic import BaseModel, EmailStr 
from datetime import datetime
from typing import Optional

#Create pydantic schema models for http request validation

# model for Admin creation and updating
class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    # role: str
    
#User Response model
class AdminResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    #convert sqlalchemy model to pydantic model, tell pydnatic model to read data even if it isnt a dictionary 
    class Config:
        orm_mode = True

# model for admin login
class AdminLogin(AdminCreate):
    pass

# model for doctor creation and updating
class DoctorBase(BaseModel):
    name: str
    email: EmailStr
    field: str
    password: str

class DoctorCreate(DoctorBase):
    pass

#response model for doctor
class DoctorResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    field: str
    created_at: datetime
    creator_id: int
    creator: AdminResponse
    class Config:
        orm_mode = True
    

# model for patient creation and updating
class PatientBase(BaseModel):
    full_name: str
    date_of_birth: int
    phone_number: str
    gender: str
    current_location: str
    email: Optional[EmailStr] = None
    
    
class PatientCreate(PatientBase):
    pass

#response model for patient 
class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    creator_id : int
    creator: AdminResponse
    class Config:
        orm_mode = True

#model for token creation        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None