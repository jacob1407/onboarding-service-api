from contextlib import contextmanager
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DB_URL)
        engine.connect()
        print("✅ Connected to the database.")
        break
    except OperationalError as e:
        wait = 2
        print(f"⏳ Waiting for DB... ({attempt + 1}/{MAX_RETRIES})")
        time.sleep(wait)
else:
    raise RuntimeError("❌ Database connection failed after several attempts.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_transactional_session():
    with transactional_session() as session:
        yield session


@contextmanager
def transactional_session():
    session = SessionLocal()
    try:
        yield session  # ← hands control to the code INSIDE the `with` block
        session.commit()  # ← resumes after `with` block finishes normally
    except:
        session.rollback()
        raise
    finally:
        session.close()
