import os
import logging
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo

MONGO_URI = os.getenv('MONGO_URI')

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://carlvinggaard:18M0n90d603@cluster0-lqr5z.mongodb.net/stockTradingGame?retryWrites=true&w=majority"
app.secret_key = 'secretkey'
mongo = PyMongo(app)

def create_user(username):
  mongo.db.users.insert({ 'username': username, 'cash': 20000.00 })
  return 

@app.route('/', methods=['POST', 'GET'])
def index():
  if 'username' in session:
    return render_template('portfolio.html', user=mongo.db.users.find_one({ 'username': session['username'] }))
  else:
    if request.method == 'POST':
      username = request.form['username'].lower()
      session['username'] = username
      exists = mongo.db.users.find_one({ 'username': username })
      if not exists:
        create_user(username)
      return redirect(url_for('index'))
    return render_template('frontpage.html')

@app.route('/history')
def history():
  return render_template('history.html', user=mongo.db.users.find_one({ 'username': session['username'] }))

@app.route('/trade')
def trade():
  return render_template('trade.html', stocks=mongo.db.stocks.find(), user=mongo.db.users.find_one({ 'username': session['username']}))

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))