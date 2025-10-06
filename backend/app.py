from routes import register_blueprints
from models import db
from flask import Flask
from flask import send_from_directory

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

app = Flask(__name__)

# Resolve instance path relative to this file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DEFAULT_SQLITE_PATH = os.path.join(INSTANCE_DIR, 'nutrition.db')
os.makedirs(INSTANCE_DIR, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', f'sqlite:///{DEFAULT_SQLITE_PATH}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Dev convenience: auto-create tables for SQLite if enabled
if os.getenv('DEV_AUTO_CREATE', '1') == '1' and app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass

# Import routes
register_blueprints(app)


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:path>')
def static_proxy(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True)
