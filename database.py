import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Loading the .env file so we can read DATABASE_URL
load_dotenv()

print("==> [database.py] Loading database configuration...", flush=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable is not set!", flush=True)
    print("Add it in Render Dashboard → Environment.", flush=True)
    sys.exit(1)

# Render/Supabase may provide postgres:// but SQLAlchemy 2.x requires postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"==> [database.py] Connecting to database at: {DATABASE_URL[:30]}...", flush=True)

try:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        connect_args={"sslmode": "require"}
    )
    print("==> [database.py] Engine created successfully", flush=True)
except Exception as e:
    print(f"ERROR creating database engine: {e}", flush=True)
    sys.exit(1)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
