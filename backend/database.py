from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv


Base = declarative_base()

connection_string = (
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
with engine.connect() as conn:
    conn.execute(text("SELECT 1"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
