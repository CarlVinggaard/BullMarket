import os
from flask import Flask, session
import unittest
from app import app
from utils import get_stock_price, is_valid_purchase, is_valid_sale, get_total_value, get_comment_counts, get_stock_data, create_user

class TestRoutesWithoutLogin(unittest.TestCase):
  
  def setUp(self):
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb+srv://test"
    self.tester = app.test_client(self)

  def test_index(self):
    response = self.tester.get("/", content_type="html/text")
    self.assertEquals(response.status_code, 200)

  def test_history_status_code(self):
    response = self.tester.get("/history", content_type="html/text")
    self.assertEquals(response.status_code, 302)

  def test_trade_redirect_works(self):
    response = self.tester.get("/trade", content_type="html/text", follow_redirects=True)
    self.assertEquals(response.status_code, 200)

''' DOESN'T WORK 
class TestRoutesWithLogin(unittest.TestCase):

  def setUp(self):
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testsecretkey"
    with app.test_client() as c:
      with c.session_transaction() as session:
        session["username"] = "testusername"

  def test_history(self):
    tester = app.test_client(self)
    response = tester.get("/history", content_type="html/text")
    self.assertEquals(response.status_code, 200) 

class TestPostRequests(unittest.TestCase):

  def setUp(self):
    app.config["TESTING"] = True

  def test_input_username(self):
    tester = app.test_client(self)
    response = tester.post("/", data=dict(username="testusername"), follow_redirects=True)
    self.assertEquals(response.status_code, 200)

class TestFunctions(unittest.TestCase):

  def setUp(self):
    app.config["TESTING"] = True

  def test_get_stock_price(self):
    priceAAPL = get_stock_price("AAPL")
    priceTSLA = get_stock_price("TSLA")
    self.assertTrue(isinstance(priceAAPL, float))
    self.assertTrue(isinstance(priceTSLA, float))

  def test_is_valid_purchase(self):
    self.assertTrue(is_valid_purchase(4, 400, 2000))
    self.assertFalse(is_valid_purchase(4, 500, 1800))
    self.assertRaises(TypeError, is_valid_purchase, "hello", 600, 1200)
    self.assertRaises(TypeError, is_valid_purchase, [200], 300, 400)
    self.assertRaises(TypeError, is_valid_purchase, { "AAPL": 1400 }, 5, 20000)

  def test_is_valid_sale(self):
    self.assertTrue(is_valid_sale(4, 8))
    self.assertFalse(is_valid_sale(10, 6))
    self.assertRaises(TypeError, is_valid_sale, "hello", 6)
    self.assertRaises(TypeError, is_valid_purchase, [2], 3)
    self.assertRaises(TypeError, is_valid_purchase, { "AAPL": 1400 }, 5)

This module can only be tested with a MonogDB database, that contains the correct stock collections.
The data model for the collection is described in the README.md file. 
class TestDatabaseCalls(unittest.TestCase):

  def test_get_total_value(self):
    value = get_total_value("testusername")
    self.assertTrue(isinstance(value, float))

  def test_get_comment_counts(self):
    data = get_stock_data()
    counts = get_comment_counts(data)
    self.assertTrue(isinstance(counts, dict))
    self.assertTrue(isinstance(counts["AAPL"], int))
    self.assertTrue(isinstance(counts["GOOG"], int)) '''
  
if __name__ == "__main__":
    unittest.main(exit=False)