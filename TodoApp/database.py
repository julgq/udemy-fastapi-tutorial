from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# conexión con sqlite
#SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# conexión con postgres
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost/postgres"

engine = create_engine(
    #solo para sqlite
    #SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}
   
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
