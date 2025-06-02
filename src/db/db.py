from contextlib import contextmanager
import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DB_URL = os.getenv("DB_URL", "")

MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        print(f"Connecting to DB at: {DB_URL}")

        engine = create_engine(DB_URL)
        engine.connect()
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
