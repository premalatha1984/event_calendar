from fastapi import APIRouter, Depends, HTTPException, Query
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
@calendar_router.post('/create_event/')
def create_event(event_data: dict, db: Session = Depends(get_db)):
    # Check if the user already has an event within the specified date range
    existing_event = db.query(models.Event).filter(
        models.Event.user_id == event_data['user_id'],
        models.Event.from_date <= event_data['to_date'],
        models.Event.to_date >= event_data['from_date']
    ).first()
    if existing_event:
        raise HTTPException(status_code=400, detail="User already has an event within the specified date range")

    # Create and save the new event
    event_data['created_by_id']=1
    event = models.Event(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return {'success': True, 'message': 'Event created successfully', 'id': event.id}

@calendar_router.get("/list_events/")
def list_events(user_id: int = Query(None, description="Filter events by user ID"), db: Session = Depends(get_db)):
    if user_id is None:
        events = db.query(models.Event).all()
    else:
        events = db.query(models.Event).filter(models.Event.user_id == user_id).all()
    
    return events