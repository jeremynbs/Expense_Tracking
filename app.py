# Code Function: Final Project
# Date: 2025/05/27, created by: 蕭智強

from flask import Flask, redirect, session
from flask_cors import CORS
from flask_session import Session
from config import Config
from db import init_db, db

# Import models to register with SQLAlchemy
from models import user, income, expense, category

# Import route blueprints
from auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.income import income_bp
from routes.expenses import expenses_bp
from routes.categories import categories_bp
from routes.reports import reports_bp

app = Flask(__name__)
app.config.from_object(Config)

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

if __name__ == "__main__":
    app.run(debug=True)
