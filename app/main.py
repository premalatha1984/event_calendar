from fastapi import FastAPI

from app.user.api import user_router
from app.calendar.api import calendar_router
app = FastAPI()


app.include_router(user_router, tags=["user_router"])
app.include_router(calendar_router, tags=["calendar_router"])

@app.get("/")
def read_root():
    return {"Hello": "login test"}
