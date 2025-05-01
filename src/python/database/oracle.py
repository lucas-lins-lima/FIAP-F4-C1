from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("ORACLE_USER")
DB_PASSWORD = os.getenv("ORACLE_PASSWORD")
DB_HOST = os.getenv("ORACLE_HOST")
DB_PORT = os.getenv("ORACLE_PORT")
DB_SERVICE = os.getenv("ORACLE_SERVICE")

DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SERVICE}"

engine = create_engine(DATABASE_URL, echo=False)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)

class DB:
    session = Session
    engine = engine

db = DB()
