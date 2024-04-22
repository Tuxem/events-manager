from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Import configuration class from config.py
from app.config import Config

# Initialize the database and migration engine
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # Load configuration settings from Config class
    app.config.from_object(Config)

    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.api import bp as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
