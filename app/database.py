# Python database connection using SQLAlchemy ORM.
# All Database Related code will be here.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "<DBMS>://<user_name>:<password>@<HostName/IP-address>/<database-name>"  <---Template
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/fastapi"

# SQL Alchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# creating a session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Adding the base that will be used anytime we will create a new table using class or python model. the class will inherit from this base.
Base = declarative_base()


# Importing the dependency
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# now we are ready to create the tables in the database using python models.
# Every python model represents a table in the database.