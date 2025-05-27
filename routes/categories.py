# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from flask import Blueprint, render_template, request, redirect, session
from db import db
from models.category import Category

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/categories", methods=["GET", "POST"])
def manage_categories():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("name")
        cat_type = request.form.get("type")
        if name and cat_type:
            new_cat = Category(name=name, type=cat_type, user_id=user_id)
            db.session.add(new_cat)
            db.session.commit()
        return redirect("/categories")

    # Group categories by type
    income_categories = Category.query.filter_by(user_id=user_id, type="income").all()
    expense_categories = Category.query.filter_by(user_id=user_id, type="expense").all()

    return render_template("categories.html", income_categories=income_categories, expense_categories=expense_categories)

@categories_bp.route("/categories/edit/<int:id>", methods=["GET", "POST"])
def edit_category(id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    category = Category.query.get_or_404(id)
    if category.user_id != user_id:
        return "Unauthorized", 403

    if request.method == "POST":
        category.name = request.form["name"]
        db.session.commit()
        return redirect("/categories")

    return render_template("edit_category.html", category=category)

@categories_bp.route("/categories/delete/<int:id>")
def delete_category(id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    category = Category.query.get_or_404(id)
    if category.user_id != user_id:
        return "Unauthorized", 403

    db.session.delete(category)
    db.session.commit()
    return redirect("/categories")
