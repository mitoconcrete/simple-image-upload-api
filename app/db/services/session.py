from sqlalchemy.orm import sessionmaker

from app.db.services.engine import engine

session = sessionmaker(bind=engine)
