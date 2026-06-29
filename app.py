import os
from flask import Flask
from dotenv import load_dotenv
from utils.db import db
from routes.auth import auth
from routes.ticket import ticket
from routes.main import main
from routes.admin import admin
from routes.profile import profile

app = Flask(__name__)

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_PERMAMENT'] = False

app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(ticket)
app.register_blueprint(main)
app.register_blueprint(admin)
app.register_blueprint(profile)