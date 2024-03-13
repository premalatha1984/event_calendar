
from sqlalchemy import Column, Integer, String,DateTime,SmallInteger,text,Date,Enum,ForeignKey
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

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(Date)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    status = Column(Enum('Busy', 'Free', 'Private', 'Public'), default='Busy')
    description = Column(String)
    user_id = Column(Integer, nullable=False)
    created_by_id = Column(Integer, nullable=False)
    updated_by_id = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    record_status = Column(SmallInteger, nullable=False, server_default=text("1"))
    deleted = Column(SmallInteger, nullable=False, server_default=text("0"))