from flask import Flask, request
from google.cloud import datastore

from command_app.app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
