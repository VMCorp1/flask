from flask import Flask
from flask import render_template, url_for, request, flash, redirect, Markup, g
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


@app.before_request
def wakeup():
    g.save_basket = False
    g.delete_basket = False
    if '/static/' in request.path:
        return
    eshop.basket_init()


@app.after_request
def sleep(response):
    if g.delete_basket:
        response.set_cookie('basket', 'deleted', 1)

    if g.save_basket:
        response.set_cookie("basket", eshop.basket_serialize())
    return response
