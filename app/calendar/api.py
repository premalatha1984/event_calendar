from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.calendar import models
calendar_router = APIRouter()

# Function to get the database session


@calendar_router.post('/create_calendar')
async def create_calendar(calendar_data: dict, db: Session = Depends(get_db)):
    if len(db.query(models.Calendar).all()) >= 25:
        raise HTTPException(status_code=400, detail="Maximum limit reached for calendars")
    
    existing_calendar = db.query(models.Calendar).filter(models.Calendar.name == calendar_data['name']).first()
    if existing_calendar:
        raise HTTPException(status_code=400, detail="Calendar name must be unique")
    calendar_data['created_by_id']=1
    calendar = models.Calendar(**calendar_data)
    db.add(calendar)
    db.commit()
    db.refresh(calendar)
    return {'success': True, 'message': 'Calendar created successfully', 'id': calendar.id}

# Endpoint to retrieve all calendar entries
@calendar_router.get('/get_all_calendars')
async def get_all_calendars(db: Session = Depends(get_db)):
    calendars = db.query(models.Calendar).all()
    return calendars

# Endpoint to retrieve a calendar entry by ID
@calendar_router.get('/get_calendar/{calendar_id}')
async def get_calendar(calendar_id: int, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == calendar_id).first()
    if calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    return calendar

# Endpoint to update a calendar entry by ID
@calendar_router.put('/update_calendar/{calendar_id}')
async def update_calendar(calendar_id: int, calendar_data: dict, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == calendar_id).first()
    if calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    for key, value in calendar_data.items():
        setattr(calendar, key, value)
    db.commit()
    db.refresh(calendar)
    return {'success': True, 'message': 'Calendar updated successfully'}

# Endpoint to delete a calendar entry by ID
@calendar_router.delete('/delete_calendar/{calendar_id}')
async def delete_calendar(calendar_id: int, db: Session = Depends(get_db)):
    calendar = db.query(models.Calendar).filter(models.Calendar.id == calendar_id).first()
    if calendar is None:
        raise HTTPException(status_code=404, detail="Calendar not found")
    db.delete(calendar)
    db.commit()
    return {'success': True, 'message': 'Calendar deleted successfully'}