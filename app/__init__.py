from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.routes import *
from app.models import *

load_dotenv()

# App Configuration
app = Flask(__name__)
CORS(app)
app.config.from_object("app.config.Config")

# Database Configuration
db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()
