from sqlalchemy.orm import sessionmaker

from app.db.engine import engine

session = sessionmaker(bind=engine)
