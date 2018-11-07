#!/usr/bin/env python

import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


basedir = os.path.abspath(os.path.dirname(__file__))

# Force development env
os.environ["FLASK_ENV"] = "development"

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

# Build the Sqlite ULR for SqlAlchemy
sqlite_url = "sqlite:///rest_api.db"

# Configure the SqlAlchemy part of the app instance
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Set other configuration
app.config["SECRET_KEY"] = 'dev'



# Configure test or prod environment


# Create the SqlAlchemy db instance
db = SQLAlchemy(app)

# Initializing Marshmallow for serialization
ma = Marshmallow(app)

DEBUG = True
FLASK_DEBUG = False
