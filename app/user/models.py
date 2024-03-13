from sqlalchemy import  Column, String, Integer,DateTime,text,SmallInteger
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by_id = Column(Integer)
    updated_by_id = Column(Integer)
    record_status = Column(SmallInteger, server_default=text("1"))
    deleted = Column(SmallInteger, server_default=text("0"))
    
    
