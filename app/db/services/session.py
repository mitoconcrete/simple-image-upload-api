from sqlalchemy.orm import sessionmaker

from app.db.services import engine

session = sessionmaker(bind=engine)
