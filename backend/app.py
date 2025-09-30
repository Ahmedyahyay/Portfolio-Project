from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///nutrition.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db
db.init_app(app)
migrate = Migrate(app, db)

# Import routes
from routes import register_blueprints
register_blueprints(app)


@app.route('/')
def index():
    return "Personal Nutrition Assistant API is running."

if __name__ == '__main__':
    app.run(debug=True)
