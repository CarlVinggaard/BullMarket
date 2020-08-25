import os
from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")

mongo = PyMongo(app)

from utils import *

''' ROUTES '''

@app.before_request
def before():
  if "username" not in session and request.endpoint != "index":
    return redirect(url_for("index"))

@app.route("/", methods=["POST", "GET"])
def index():
  ''' If logged in, go to portfolio, else go to front page'''
  if "username" in session:
    return render_template("portfolio.html", data=get_stock_data(), user=mongo.db.users.find_one({ "username": session["username"] }),
      value=get_total_value(session["username"]))
  else:
    if request.method == "POST":
      username = request.form["username"].lower()
      session["username"] = username

      ''' Try to find an existing user, otherwise create one. '''
      exists = mongo.db.users.find_one({ "username": username })
      if not exists:
        create_user(username)

      return redirect(url_for("index"))
    return render_template("frontpage.html")

@app.route("/history")
def history():
  return render_template("history.html", user=mongo.db.users.find_one({ "username": session["username"] }))

@app.route("/trade")
def trade():
  data = get_stock_data()
  comments = get_comment_counts(data)
  return render_template("trade.html", data=data, user=mongo.db.users.find_one({ "username": session["username"]}), comments=comments)
  
@app.route("/buy/<stock_code>", methods=["GET", "POST"])
def buy(stock_code):
  user = mongo.db.users.find_one({ "username": session["username"]})
  price = get_stock_price(stock_code)
  total = 0
  quantity = 0
  error = ""
  if request.method == "POST":
    quantity = int(request.form["quantity"])
    total = quantity * price

    ''' If 'buy' is not in the form, we are simply calculating the price. '''
    if "buy" in request.form:

      ''' Either purchase the stock or set an error. '''
      if is_valid_purchase(quantity, price, user["cash"]):
        buy_stock(stock_code, quantity, price)
        update_value_at_last_trade()
        return redirect(url_for("index"))
      else:
        error = "You don't have enough money for that."
  return render_template("buy.html", user=user, stock=stock_code, price=price, total=total, quantity=quantity, error=error)

@app.route("/sell/<stock_code>", methods=["GET", "POST"])
def sell(stock_code):
  user = mongo.db.users.find_one({ "username": session["username"] })
  try:
    stock_quantity = [stock["quantity"] for stock in user["portfolio"] if stock["stockCode"] == stock_code][0]
  except:
    stock_quantity = 0
  price = get_stock_price(stock_code)
  total = 0
  quantity = 0
  error = ""
  if request.method == "POST":
    quantity = int(request.form["quantity"])
    total = quantity * price

    ''' If 'sell' is not in the form, we are simply calculating the price. '''
    if "sell" in request.form:

      ''' Either sell the stock or set an error. '''
      if is_valid_sale(quantity, stock_quantity):
        sell_stock(stock_code, quantity, price)
        update_value_at_last_trade()
        return redirect(url_for("index"))
      else:
        error = "You don't have that much of this stock."
  return render_template("sell.html", user=user, stock=stock_code, price=price, total=total, quantity=quantity, error=error,
    stock_quantity=stock_quantity)

@app.route("/stocks/<stock_code>", methods=["GET", "POST"])
def stock(stock_code):
  user = mongo.db.users.find_one({ "username": session["username"] })
  price = get_stock_price(stock_code)
  stock = mongo.db.stocks.find_one({ "stockCode": stock_code })
  comments = mongo.db.comments.find({ "stockCode": stock_code }).sort("createdAt")
  editing_id = ""
  ''' If 'delete' -> delete,
      if 'edit' -> update a comment and stop editing,
      if 'editing' -> set editing state,
      if 'comment' -> post comment. '''
  if request.method == "POST":
    if "delete" in request.form:
      delete_comment(request.form["delete"])
    elif "edit" in request.form:
      edit_comment(request.form["editing"], request.form["edit"])
      editing_id = ""
    elif "editing" in request.form:
      editing_id = ObjectId(request.form["editing"])
    elif "comment" in request.form:
      add_comment(request.form["comment"], stock_code)
    else:
      return request.form
  return render_template("stock.html", user=user, price=price, stock=stock, comments=comments, editing=editing_id)

@app.route("/logout")
def logout():
  session.pop("username", None)
  return redirect(url_for("index"))


if __name__ == "__main__":
  app.run(host=os.getenv("IP"),
    port=int(os.getenv("PORT")),
    debug=True)
            