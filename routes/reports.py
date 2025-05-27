# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from flask import Blueprint, render_template, request, session, send_file
from db import db
from models.income import Income
from models.expense import Expense
from models.category import Category
from io import StringIO, BytesIO
import csv
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/reports", methods=["GET"])
def reports_page():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    start = request.args.get("start")
    end = request.args.get("end")
    entry_type = request.args.get("type", "income")

    model = Income if entry_type == "income" else Expense
    query = model.query.filter_by(user_id=user_id)

    if start:
        query = query.filter(model.date >= start)
    if end:
        query = query.filter(model.date <= end)

    records = query.order_by(model.date.desc()).all()
    categories = {c.id: c.name for c in Category.query.filter_by(user_id=user_id).all()}

    return render_template("reports.html", records=records, entry_type=entry_type, categories=categories)

@reports_bp.route("/reports/export/<fmt>")
def export_report(fmt):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    start = request.args.get("start")
    end = request.args.get("end")
    entry_type = request.args.get("type", "income")

    model = Income if entry_type == "income" else Expense
    query = model.query.filter_by(user_id=user_id)

    if start:
        query = query.filter(model.date >= start)
    if end:
        query = query.filter(model.date <= end)

    records = query.order_by(model.date.desc()).all()

    if fmt == "csv":
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["Date", "Amount", "Category", "Description"])
        for r in records:
            writer.writerow([r.date, r.amount, r.category.name, r.description])
        output.seek(0)
        return send_file(BytesIO(output.read().encode()), mimetype="text/csv", as_attachment=True, download_name="report.csv")

    elif fmt == "pdf":
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.drawString(50, 750, "Expense Tracker Report")
        y = 720
        for r in records:
            text = f"{r.date} - ${r.amount} - {r.category.name} - {r.description or ''}"
            pdf.drawString(50, y, text)
            y -= 20
            if y < 50:
                pdf.showPage()
                y = 750
        pdf.save()
        buffer.seek(0)
        return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name="report.pdf")

    return "Invalid format", 400
