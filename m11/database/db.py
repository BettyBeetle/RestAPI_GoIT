from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import os

config = configparser.ConfigParser()
try:
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
    db_user = config.get('database', 'db_user')
    db_password = config.get('database', 'db_password')
    db_host = config.get('database', 'db_host')
    db_port = config.get('database', 'db_port')
    db_name = config.get('database', 'db_name')
    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
except Exception as e:
    print(f"Error reading config file: {e}")
    raise e


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
