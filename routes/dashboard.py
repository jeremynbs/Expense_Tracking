# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from flask import Blueprint, jsonify, session, redirect, render_template
from db import db
from models.income import Income
from models.expense import Expense
from models.category import Category
from datetime import date, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard_view():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    return render_template("dashboard.html")


@dashboard_bp.route("/api/dashboard-data")
def dashboard_data():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    today = date.today()
    start_month = today.replace(day=1)
    last_10_days = [today - timedelta(days=i) for i in range(9, -1, -1)]

    # Query income and expenses for the current user
    income = Income.query.filter_by(user_id=user_id).all()
    expense = Expense.query.filter_by(user_id=user_id).all()

    # Filter this month's data
    monthly_income = [i for i in income if i.date >= start_month]
    monthly_expense = [e for e in expense if e.date >= start_month]

    total_income = sum(i.amount for i in monthly_income)
    total_expense = sum(e.amount for e in monthly_expense)
    balance = total_income - total_expense

    # Balance trend (last 10 days)
    trend_labels = [d.strftime("%b %d") for d in last_10_days]
    trend_values = []
    for d in last_10_days:
        daily_income = sum(i.amount for i in income if i.date == d)
        daily_expense = sum(e.amount for e in expense if e.date == d)
        daily_balance = daily_income - daily_expense
        trend_values.append(float(daily_balance))

    # Pie charts by category
    def pie_data(records, type_filter):
        categories = Category.query.filter_by(user_id=user_id, type=type_filter).all()
        cat_map = {c.id: c.name for c in categories}
        totals = {}
        for r in records:
            name = cat_map.get(r.category_id, "Unknown")
            totals[name] = totals.get(name, 0) + float(r.amount)
        return {
            "labels": list(totals.keys()),
            "values": list(totals.values())
        }

    return jsonify({
        "balance": float(balance),
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "balance_trend": {
            "labels": trend_labels,
            "values": trend_values
        },
        "income_by_category": pie_data(monthly_income, "income"),
        "expense_by_category": pie_data(monthly_expense, "expense")
    })
