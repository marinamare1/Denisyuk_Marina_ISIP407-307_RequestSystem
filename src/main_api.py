import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI
from src.api import requests

app = FastAPI(
    title="Система учёта заявок",
    description="REST API для системы учёта заявок",
    version="1.0.0",
)

app.include_router(requests.router)