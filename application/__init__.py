from flask import Flask
from flask import render_template, url_for, request, flash, redirect, Markup
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "12341231234"

app.config.from_object(__name__)

db = SQLAlchemy(app)
from application.schema import Catalog, Order, OrderItem, User
db.create_all()

import application.lib as eshop
import application.routes