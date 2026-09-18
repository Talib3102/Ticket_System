import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Loading the .env file so we can read DATABASE_URL
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set. "
                       "Add it in Render Dashboard → Environment.")

# Render/Supabase may provide postgres:// but SQLAlchemy 2.x requires postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Supabase requires SSL for external connections
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
