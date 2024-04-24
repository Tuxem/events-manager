import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.database import db, migrate
from app.config import Config
from app.routes.api import api as api_blueprint
from app.routes.web import web

def create_app():
    app = Flask(__name__)
    # Load configuration settings from Config class
    app.config.from_object(Config)

    print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])
    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    app.register_blueprint(web)


    # Configure logging
    # Set up logging
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)  # Adjust as needed
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)    
    app.logger.info('MyApp startup')

    return app
