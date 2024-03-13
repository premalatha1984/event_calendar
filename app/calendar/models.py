
from sqlalchemy import Column, Integer, String,DateTime,SmallInteger,text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Calendar(Base):
    __tablename__ = 'calendar'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    timezone = Column(String, nullable=False)
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))