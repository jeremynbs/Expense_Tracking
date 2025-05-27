# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from db import db
from datetime import datetime
from models.category import Category

class Income(db.Model):
    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    description = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

    category = db.relationship("Category", backref="income")

    def __repr__(self):
        return f"<Income ${self.amount} on {self.date}>"
