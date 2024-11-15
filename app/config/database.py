from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .env import env

engine = create_engine(
    env.DB_URL,
    connect_args={'check_same_thread': False},
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Base = declarative_base()


def get_db():
    """
    Create a database session.
    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
