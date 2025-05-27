# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

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

@expenses_bp.route("/expenses/edit/<int:id>", methods=["GET", "POST"])
def edit_expense(id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    record = Expense.query.get_or_404(id)
    if record.user_id != user_id:
        return "Unauthorized", 403

    if request.method == "POST":
        record.amount = request.form["amount"]
        record.date = date.fromisoformat(request.form["date"])
        record.category_id = request.form["category_id"]
        record.description = request.form["description"]
        db.session.commit()
        return redirect("/expenses")

    categories = Category.query.filter_by(user_id=user_id, type="expense").all()
    return render_template("edit_expense.html", record=record, categories=categories)


@expenses_bp.route("/expenses/delete/<int:id>")
def delete_expense(id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    record = Expense.query.get_or_404(id)
    if record.user_id != user_id:
        return "Unauthorized", 403

    db.session.delete(record)
    db.session.commit()
    return redirect("/expenses")
