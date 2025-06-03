# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from flask import Flask, redirect, session, request
import subprocess
from flask_cors import CORS
from flask_session import Session
from config import Config
from db import init_db, db
import os

# Import route blueprints
from auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.income import income_bp
from routes.expenses import expenses_bp
from routes.categories import categories_bp
from routes.reports import reports_bp

app = Flask(__name__)
app.config.from_object(Config)

app.config["SESSION_COOKIE_SECURE"] = os.getenv("SESSION_COOKIE_SECURE", "False") == "True"


# Init CORS, sessions, DB
CORS(app)
Session(app)
init_db(app)

# Register all routes
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(income_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(reports_bp)

# Root page (optional)
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    return redirect("/dashboard")

# Webhook for auto-updating the app 
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("X-GitHub-Event") == "push":
        subprocess.run(["git", "pull"], cwd="/root/Expense_Tracking")
        subprocess.run(["systemctl", "restart", "expense-app"])
        return "Updated", 200
    return "Ignored", 400

if __name__ == "__main__":
    app.run(debug=True)
