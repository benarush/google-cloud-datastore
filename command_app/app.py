from flask import Flask, request
from google.cloud import datastore
from command_app.api.commands_apis import commands_bp
from command_app.extensions import gcp_db


def register_extensions(app: Flask):
    # bind it to app, to avoiding importing it at project level, not actually needed but if wanting
    # to implement DI in future
    app.extensions['GCP_DATASTORE'] = gcp_db


def register_apis(app):
    app.register_blueprint(commands_bp)


def create_app(config_object='command_app.settings') -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_apis(app)
    return app
