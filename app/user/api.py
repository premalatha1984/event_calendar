from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from app.database import SessionLocal, get_db
from app.user.schemas import EmailCreate, JsonData
from app.user.models import Email
from email.message import EmailMessage
from aiosmtplib import send
from email import encoders
from sqlalchemy.orm import Session



user_router = APIRouter()


@user_router.post('/save_email')
async def save_email(email_data: EmailCreate, db: SessionLocal = Depends(get_db)): # type: ignore
    # Check if the email already exists in the database
    existing_email = db.query(Email).filter(
        Email.email == email_data.email).first()

    if existing_email:
        return {'success': True, 'message': 'Email already exists', 'id': existing_email.id}

    # Create an instance of the Email model
    new_email = Email(email=email_data.email)

    # Add the new email to the database
    db.add(new_email)
    db.commit()
    db.refresh(new_email)

    return {'success': True, 'message': 'Email saved successfully', 'id': new_email.id}

