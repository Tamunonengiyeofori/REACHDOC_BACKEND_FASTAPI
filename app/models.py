#THIS FILE HANDLES DATABASE TABLE CREATION USING ORM MODELS AND SQLALCHEMY

from .database import Base
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

#create a User model for admin user
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True , nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False, server_default="admin")
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True , nullable=False) 
    full_name = Column(String, nullable=False)
    date_of_birth = Column(Integer, nullable=False)
    phone_number = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    current_location = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False, server_default="patient")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    creator_id = Column(Integer,ForeignKey("admins.id", ondelete="CASCADE"), nullable=False)
    creator = relationship("Admin")


class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    field = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="doctor")
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default="now()")
    creator_id = Column(Integer, ForeignKey("admins.id", ondelete="CASCADE"), nullable=False)
    creator = relationship("Admin")
    
    
