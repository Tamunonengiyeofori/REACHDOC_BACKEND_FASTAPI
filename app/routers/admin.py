#THIS FILE HANDLES ALL PATH OPERATIONS FOR USERS

from .. import models, schemas, utils
from fastapi import FastAPI,  status, HTTPException, Response, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

#create a router object from the APIRouter class
router = APIRouter(
    prefix="/admin",
    tags = ["Admins"]
)

# Create a path operation for creating an Admin
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
def create_admin(admin: schemas.AdminCreate , db: Session = Depends(get_db)):
    # hash admin password (admin.password)
    admin_password = utils.hash(admin.password)
    #update user password 
    admin.password = admin_password
    new_admin = models.Admin(**admin.dict())
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

#Create a path operation for getting aa Admin by id
@router.get("/{id}", response_model=schemas.AdminResponse)
def get_(id: int , db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.id == id).first()
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"admin with id: {id} does not exist")
    return admin