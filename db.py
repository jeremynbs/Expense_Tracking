# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

