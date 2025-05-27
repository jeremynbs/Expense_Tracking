# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///data.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
