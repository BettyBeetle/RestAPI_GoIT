from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contacts(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, index=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    nick = Column(String, nullable=True, default=None)