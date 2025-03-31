from command_app.settings import *  # noqa
from google.cloud import datastore

gcp_db = datastore.Client()


