#THIS FILE HANDLES POSTGRESQL DATABASE CONNECTION USING SQLALCHEMY

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

POSTGRES_PSWD = os.getenv("postgress_password")

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)
Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# #Keep looping connection until the connection to the datbase is successful then create API server
# while True:
#     try: 
#         connection = psycopg2.connect(host="localhost" ,
#                                       database="Medicals" ,
#                                       user="postgres" ,
#                                       password=POSTGRES_PSWD ,
#                                       cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Succesfully connected to the database!!!!!")
#         break
    
#     except Exception as error:
#         print('Database connection not successfull !!!')
#         print(f"Error: {error}")
#         # Delay reconnection trial by a little time
#         time.sleep(3)