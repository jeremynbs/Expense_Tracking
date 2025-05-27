# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from flask import Blueprint, request, session, jsonify, redirect, render_template, current_app
import requests
from db import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

# Google ID token POST endpoint
@auth_bp.route("/api/login", methods=["POST"])
def login():
    # ✅ Ensure JSON payload
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    token = request.json.get("id_token")
    if not token:
        return jsonify({"error": "No ID token provided"}), 400

    try:
        print("Received token:", token)

        response = requests.get(GOOGLE_TOKEN_INFO_URL, params={"id_token": token})
        print("Google response status:", response.status_code)

        if response.status_code != 200:
            return jsonify({"error": "Invalid ID token"}), 401

        data = response.json()
        print("Decoded token:", data)

        google_id = data["sub"]
        email = data.get("email")
        name = data.get("name", "")
        picture = data.get("picture", "")

        user = User.query.filter_by(google_id=google_id).first()
        print("User found:", user)

        if not user:
            print("Creating new user...")
            user = User(google_id=google_id, email=email, name=name, picture=picture)
            db.session.add(user)
            db.session.commit()

        session["user_id"] = user.id
        print("Session set with user_id:", user.id)

        return jsonify({"message": "Login successful", "user": {"name": name, "email": email}})


    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Server error during login"}), 500

# 🧼 Logout with session clear
@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})

# 🎯 Serve login page
@auth_bp.route("/login")
def login_page():
    return render_template("login.html", google_client_id=current_app.config["GOOGLE_CLIENT_ID"])
