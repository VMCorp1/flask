from flask import Flask
from flask import render_template, url_for


app = Flask(__name__)
import application.routes
DEBUG = True
app.config.from_object(__name__)
