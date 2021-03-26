"""main app init"""
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import config
from .DoList.views import blueprint_DoList


db = SQLAlchemy()
migrate = Migrate()
from DoList.DoList.models import *


def create_app(config_name):
    """An application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    blueprint_registration(app)
    api = Api(app)
    resource_adding(api)
    return app


def blueprint_registration(app):
    """Register Flask blueprints"""
    app.register_blueprint(blueprint_DoList, url_prefix='/')


def resource_adding(api):
    """Resource adding"""
    from .DoList.resources.api import ItemsResource
    api.add_resource(ItemsResource, '/api/dolist')


