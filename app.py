from flask import render_template, request, session, redirect, url_for
from bson.objectid import ObjectId
from utils import *

app = create_flask_app()

# ROUTES
@app.route('/', methods=['POST', 'GET'])
def index():
  if 'username' in session:
    return render_template('portfolio.html', data=get_stock_data(), user=mongo.db.users.find_one({ 'username': session['username'] }), value=get_total_value(session['username']))
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
  if 'username' in session:
    return render_template('history.html', user=mongo.db.users.find_one({ 'username': session['username'] }))
  else:
    return redirect(url_for('index'))

@app.route('/trade')
def trade():
  if 'username' in session:
    data = get_stock_data()
    comments = get_comment_counts(data)
    return render_template('trade.html', data=data, user=mongo.db.users.find_one({ 'username': session['username']}), comments=comments)
  else:
    return redirect(url_for('index'))
  
@app.route('/buy/<stockCode>', methods=['GET', 'POST'])
def buy(stockCode):
  if 'username' in session:
    user = mongo.db.users.find_one({ 'username': session['username']})
    price = get_stock_price(stockCode)
    total = 0
    quantity = 0
    error = ''
    if request.method == "POST":
      quantity = int(request.form["quantity"])
      total = quantity * price
      if 'buy' in request.form:
        if is_valid_purchase(quantity, price, user['cash']):
          buy_stock(stockCode, quantity, price)
          update_value_at_last_trade()
          return redirect(url_for('index'))
        else:
          error = "You don't have enough money for that."
    return render_template('buy.html', user=user, stock=stockCode, price=price, total=total, quantity=quantity, error=error)
  else:
    return redirect(url_for('inde'))

@app.route('/sell/<stockCode>', methods=['GET', 'POST'])
def sell(stockCode):
  if 'username' in session:
    user = mongo.db.users.find_one({ 'username': session['username'] })
    try:
      stockQuantity = [stock['quantity'] for stock in user['portfolio'] if stock['stockCode'] == stockCode][0]
    except:
      stockQuantity = 0
    price = get_stock_price(stockCode)
    total = 0
    quantity = 0
    error = ''
    if request.method == "POST":
      quantity = int(request.form["quantity"])
      total = quantity * price
      if 'sell' in request.form:
        if is_valid_sale(quantity, stockQuantity):
          sell_stock(stockCode, quantity, price)
          update_value_at_last_trade()
          return redirect(url_for('index'))
        else:
          error = "You don't have that much of this stock."
    return render_template('sell.html', user=user, stock=stockCode, price=price, total=total, quantity=quantity, error=error, stockQuantity=stockQuantity)
  else:
    return redirect(url_for('index'))

@app.route('/stocks/<stockCode>', methods=['GET', 'POST'])
def stock(stockCode):
  if 'username' in session:
    user = mongo.db.users.find_one({ 'username': session['username'] })
    price = get_stock_price(stockCode)
    stock = mongo.db.stocks.find_one({ 'stockCode': stockCode })
    comments = mongo.db.comments.find({ 'stockCode': stockCode }).sort('createdAt')
    editingId = ''
    if request.method == 'POST':
      if 'delete' in request.form:
        delete_comment(request.form['delete'])
      elif 'edit' in request.form:
        edit_comment(request.form['editing'], request.form['edit'])
        editingId = ''
      elif 'editing' in request.form:
        editingId = ObjectId(request.form['editing'])
      elif 'comment' in request.form:
        add_comment(request.form['comment'], stockCode)
      else:
        return request.form
    return render_template('stock.html', user=user, price=price, stock=stock, comments=comments, editing=editingId)
  else:
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host=os.getenv('IP'),
            port=int(os.getenv('PORT')),
            debug=True)
            