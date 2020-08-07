import os
from flask import Flask, render_template
from flask_pymongo import PyMongo

MONGO_URI = os.getenv('MONGO_URI')

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

@app.route('/')
def front_page():
  return render_template('base.html')
