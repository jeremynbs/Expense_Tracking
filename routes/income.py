# routes/income.py

from flask import Blueprint, render_template, request, redirect, session
from db import db
from models.income import Income
from models.category import Category
from datetime import date

income_bp = Blueprint("income", __name__)

@income_bp.route("/income", methods=["GET"])
def income_page():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    # Load categories for dropdown
    categories = Category.query.filter_by(user_id=user_id, type="income").all()

    # Load income records
    income_records = Income.query.filter_by(user_id=user_id).order_by(Income.date.desc()).all()
    print(income_records)

    return render_template("income.html", categories=categories, income_records=income_records)

@income_bp.route("/income/add", methods=["POST"])
def add_income():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    amount = request.form.get("amount")
    date_value = request.form.get("date")
    category_id = request.form.get("category_id")
    description = request.form.get("description", "")

    new_income = Income(
        amount=amount,
        date=date.fromisoformat(date_value),
        user_id=user_id,
        category_id=category_id,
        description=description
    )
    db.session.add(new_income)
    db.session.commit()

    return redirect("/income")
