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




user_router = APIRouter()


