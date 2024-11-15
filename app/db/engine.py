from sqlalchemy import create_engine

from app.configs.setting import setting

engine = create_engine(setting.DB_URL, echo=True)
