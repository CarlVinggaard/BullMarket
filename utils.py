import os
from flask import Flask, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import yfinance as yf
from app import mongo

''' FUNCTIONS '''

def get_stock_data():
  ''' Get data for all stocks in database, using the yfinance API. '''
  stock_code_array = []
  stocks = mongo.db.stocks.find()
  for stock in stocks:
    stock_code_array.append(stock["stockCode"])
  
  ''' Get data from API. '''
  data = yf.download(stock_code_array, period="1d")
  get_stock_tuple = lambda code: (code, round(data[("Close", code)][0], 2))
  stock_price_dict = dict(map(get_stock_tuple, stock_code_array))
  return stock_price_dict

''' Get price for a single stock. '''
def get_stock_price(stock_code):
  data = yf.download(stock_code, period="d1")
  return round(data["Close"][0], 2)

''' Get the total value of a user's stock portfolio (excluding cash). '''
def get_total_value(username):
  user = mongo.db.users.find_one({ "username": username })
  data = get_stock_data()

  get_stock_value = lambda stock: stock["quantity"] * data[stock["stockCode"]]

  return round(sum(list(map(get_stock_value, user["portfolio"]))), 2)

''' Get a dictionary mapping all stocks to the number of comments on them. '''
def get_comment_counts(data):
  comments = {}
  for stock in data:
    count = mongo.db.comments.count({ "stockCode": stock })
    comments[stock] = count
  return comments
    
''' Return a boolean describing if a user has cash for a purchase. '''
def is_valid_purchase(quantity, price, cash):
  return quantity * price <= cash

''' Return a boolean describing if a user has enough stock for a sale '''
def is_valid_sale(quantity, stock_quantity):
  return stock_quantity >= quantity

''' Add a trade to the database. '''
def add_trade(stock_code, quantity, buy_or_sell, price):
  trade = { "stockCode": stock_code, "quantity": quantity, "type":  buy_or_sell, "price": price, "timestamp": datetime.now() }
  mongo.db.users.update_one({ "username": session["username"] }, { "$push": { "trades": trade } })

''' Add stock to a user portfolio and subtract the cash. '''
def buy_stock(stock_code, quantity, price):
  ''' If there is no object with this stock code in the portfolio, create one. '''
  mongo.db.users.update({ "username": session["username"], "portfolio.stockCode": { "$ne": stock_code } }, 
    { "$push": { "portfolio": { "stockCode": stock_code, "quantity": 0 } } })
 
  ''' Increment the portfolio with <quantity>. '''
  query = { "username": session["username"], "portfolio.stockCode": stock_code }
  value = { "$inc": { "portfolio.$.quantity": quantity } }
  mongo.db.users.update_one(query, value)

  ''' Subtract the cash. '''
  mongo.db.users.update({ "username": session["username"]}, { "$inc": { "cash": -(quantity * price) } })

  ''' Add trade to history. '''
  add_trade(stock_code, quantity, "buy", price)

''' Subtract the stock from a user portfolio and add the cash. '''
def sell_stock(stock_code, quantity, price):
  ''' Decrement the portfolio with <quantity>. '''
  query = { "username": session["username"], "portfolio.stockCode": stock_code }
  value = { "$inc": { "portfolio.$.quantity": -quantity } }
  mongo.db.users.update_one(query, value)

  ''' Add the cash. '''
  mongo.db.users.update({ "username": session["username"]}, { "$inc": { "cash": quantity * price } })

  ''' Add trade to history. '''
  add_trade(stock_code, quantity, "sell", price)

''' Update the valueAtLastTrade for a user. '''
def update_value_at_last_trade():
  user = mongo.db.users.find_one({ "username": session["username"] })
  cash = user["cash"]
  total = get_total_value(session["username"]) + cash
  mongo.db.users.update_one({ "username": session["username"] }, { "$set": { "valueAtLastTrade": total } })

def create_user(username):
  mongo.db.users.insert({ "username": username, "cash": 20000.00, "portfolio": [] })

def add_comment(content, stock_code):
  mongo.db.comments.insert({ "content": content, "stockCode": stock_code, "createdAt": datetime.now(), "username": session["username"] })

def delete_comment(id):
  mongo.db.comments.delete_one({ "_id": ObjectId(id) })

def edit_comment(id, content):
  mongo.db.comments.update_one({ "_id": ObjectId(id) }, { "$set": { "content": content } })

