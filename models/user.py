from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    full_name = Column(String)
    source = Column(String)
    first_seen = Column(DateTime)
    last_active = Column(DateTime)
    visit_count = Column(Integer)
