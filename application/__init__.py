from flask import Flask
from flask import render_template, url_for, request, flash, redirect, Markup

import application.lib as eshop

app = Flask(__name__)
import application.routes
DEBUG = True
app.config.from_object(__name__)
import application.lib as eshop

SECRET_KEY = "12341231234"
app.secret_key = SECRET_KEY