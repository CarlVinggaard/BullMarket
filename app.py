import os
from flask import Flask, render_template
from flask_pymongo import PyMongo

MONGO_URI = os.getenv('MONGO_URI')

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

@app.route('/')
def portfolio():
  return render_template('portfolio.html')

@app.route('/history')
def history():
  return render_template('history.html')

@app.route('/trade')
def trade():
  return render_template('trade.html')

@app.route('/frontpage')
def front_page():
  return render_template('frontpage.html')