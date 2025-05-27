# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    picture = db.Column(db.String(512))  # optional profile image from Google

    def __repr__(self):
        return f"<User {self.email}>"
