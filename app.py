# from flask import Flask
# from config import Config
# from db import init_db

# # Import route blueprints
# from routes.dashboard import dashboard_bp
# from routes.income import income_bp
# from routes.expenses import expenses_bp
# from routes.categories import categories_bp
# from routes.reports import reports_bp
# from auth import auth_bp

# app = Flask(__name__)
# app.config.from_object(Config)

# # Initialize PostgreSQL connection
# init_db(app)

# # Register Blueprints
# app.register_blueprint(auth_bp)
# app.register_blueprint(dashboard_bp)
# app.register_blueprint(income_bp)
# app.register_blueprint(expenses_bp)
# app.register_blueprint(categories_bp)
# app.register_blueprint(reports_bp)

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask
from flask_cors import CORS
from flask_session import Session

from config import Config
from db import init_db

from db import db
from models import user  # Add this line after db is initialized


app = Flask(__name__)
app.config.from_object(Config)

# Setup CORS and session
CORS(app)
Session(app)

# Initialize PostgreSQL connection
init_db(app)

@app.route("/")
def index():
    return "✅ Flask app is running!"

if __name__ == "__main__":
    app.run(debug=True)
