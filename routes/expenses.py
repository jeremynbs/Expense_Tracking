# routes/expenses.py

from flask import Blueprint, render_template, request, redirect, session
from db import db
from models.expense import Expense
from models.category import Category
from datetime import date

expenses_bp = Blueprint("expenses", __name__)

@expenses_bp.route("/expenses", methods=["GET"])
def expenses_page():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    categories = Category.query.filter_by(user_id=user_id, type="expense").all()
    expense_records = Expense.query.filter_by(user_id=user_id).order_by(Expense.date.desc()).all()

    return render_template("expenses.html", categories=categories, expense_records=expense_records)

@expenses_bp.route("/expenses/add", methods=["POST"])
def add_expense():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    amount = request.form.get("amount")
    date_value = request.form.get("date")
    category_id = request.form.get("category_id")
    description = request.form.get("description", "")

    new_expense = Expense(
        amount=amount,
        date=date.fromisoformat(date_value),
        user_id=user_id,
        category_id=category_id,
        description=description
    )
    db.session.add(new_expense)
    db.session.commit()

    return redirect("/expenses")
