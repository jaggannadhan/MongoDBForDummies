from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import logging

default_router = APIRouter()
logger = logging.getLogger(__name__)

# Configure Jinja2Templates to look for HTML files in the "templates" folder
templates = Jinja2Templates(directory="templates")

# Example route to test the MongoDB connection
@default_router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})