# Bull Market

Bull Market is a stock trading game. Practice your stock trading skills on real stocks, with fake money. Start with $20,000 and buy or sell stocks to grow the value of your portfolio.

## UX
 
The UX process involved 1) identifying the overall user goal, 2) defining a few user stories that support this goal and 3) making a prototype design.

The overall user goal with the game is to practice buying and selling stocks. The specific user stories that support this goal are:

1) As a user, I want to be able to buy and sell stocks.
2) As a user, I want to get a clear and simple overview of my portfolio and whether or not I've lost money in the game.
3) As a user, I want to be able to interact with the community and discuss stocks.

A prototype was made in Figma, a wireframing program. It can be seen at https://www.figma.com/file/M1r5m0fqqQbS5SbFkx8ZqYKN/Bull-Market?node-id=0%3A1

### Existing Features
- User creation and login - To start with, a user can enter a username. Entering a new username creates a new user, while entering an existing username logs the user in.
- Stock listing - Allows the user to see all stocks in the game.
- Single stock view - Allows the user to get an overview of a single stock, including a description of the company.
- Comments - The comments section allows the players to interact with each other by commenting about specific stocks. This includes ability to edit and delete one's own comments.
- Portfolio overview - The 'portfolio' page gives the user a clear overview over their current portfolio, including total value and all stock quantities.
- Trade history - The 'history' page gives the user a a historical overview of all their trades and relevant information.
- Navbar - Allows easy navigation throughout the application and is mobile-friendly. 

### Features Left to Implement
- User profile - An overview over one's own profile.
- Secure login - user login with password.
- Trending data for stocks - Historical time series data for each stock would improve the game.
- More current data - Due to API limitations, the current version of the game features only daily updates of stock prices. Live updated data would make the game more interesting and real.

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    - The project uses **Flask** as the main framework for the web application. It includes a server interface (WSGI), a routing system and a language for writing HTML templates (Jinja).
- [MongoDB](https://www.mongodb.com/)
  - **MongoDB** is used as a database. It is a NoSQL, document-based database, made for storing very large amounts of data.
- [yfinance](https://pypi.org/project/yfinance/)
  - The game relies on the stock API **yfinance** to get stock data. It is a wrapper for the Yahoo Finance API, which has been decommissioned.
- [Python module: venv](https://docs.python.org/3/tutorial/venv.html)
  - **Venv** is a virtual environment used to guanrantee a functioning environment during development.
- [Flask-PyMongo](https://flask-pymongo.readthedocs.io/en/latest/)
  - The **Flask-PyMongo** library is used to easily connect the flask application the the database.
- [unittest](https://docs.python.org/3/library/unittest.html)
  - The **Unittest** python module has been used for automated testing.

## Testing

### User goal testing

Important tests of the user's ability to complete their goals are:

- Try to create a new user from the front page
  - Check that entering a username and clicking 'start trading' directs to the portfolio page.
  - Check that there is $20000 cash and an empty portfolio.
  - Check that the correct username is written in the top right corner.

- Buy some stock
  - Click the 'buy' button (from the 'portfolio' or 'trade' pages) and check that directs to '/buy/<stockCode>'.
  - Enter a quantity of stock, click 'calculate price' and checks that a correct value is displayed.
  - Click 'buy', check that it redirects to the 'portfolio' page, and that the correct quantity of stock has been added to the portfolio.
  - Enter a too high quantity of stock (total value > available cash), click 'buy', and check that an error is displayed.
  - Go to '/history' and check that any successful purchases have been added to the page.

- Sell some stock
  - Click the 'sell' button (from the 'portfolio' or 'trade' pages) and check that directs to '/sell/<stockCode>'.
  - Enter a quantity of stock, click 'calculate price' and checks that a correct value is displayed.
  - Click 'sell', check that it redirects to the 'portfolio' page, and that the correct quantity of stock has been removed to the portfolio.
  - Enter a too high quantity of stock (quantity > current quantity in portfolio), click 'sell', and check that an error is displayed.
  - Go to '/history' and check that any successful purchases have been added to the page.

- Write a comment
  - Go to a stock, write a comment, and click 'comment'.
  - Check that the 'edit' and 'delete' buttons are there for the users own comments, but not for others.
  - Check that username and timestamp are displayed correctly.

- Update a comment
  - Go to a stock that the user has commented on.
  - Click 'update' next to one of the user's own comments.
  - Edit the comment in the input box and click 'update'.
  - Check that the comment has been updated.

- Delete a comment
  - Go to a stock that the user has commented on.
  - Click 'delete' next to one of the user's own comments.
  - Check that the comment has been deleted.


### Unit testing

Automatic unit testing of certain functions has been implemented using the 'unittest' module. These can be found in tests/test.py.
These tests helped make sure that the functions would work and return the correct errors if given wrong input.

In order to execute the functions, a valid MONGO_URI environment variable must be defined in the terminal. One option is to enter a fake URI:
> export MONGO_URI="mongodb://test"

This will make the test run (without failures), but it will have errors because the correct collections won't be found in mongo. 
Alternatively, use a real URI for a MongoDB with the collections 'users', 'stocks' and 'comments' (see the data model below for more detail).

When this is done, execute the tests with the command:
> 'python3 -m unittest tests/test.py'

### Testing different devices and browsers

The application has been tested with different browsers and on a variety of screens:

- Mobile: OnePlus 6T, using Google Chrome.
- Laptop: MacBook Pro, MacOs, using Safari.
- Desktop Asus, Windows 10, using Firefox.

## Deployment

The project is deployed to Heroku, at https://bull-market.herokuapp.com/.

It takes advantage of Heroku's option to deploy automatically from a Github repository. Updates to the master branch will thus be deployed automatically to the live app.

Required environment variables are:
  1. **MONGO_URI** - the link to the mongoDB database
  2. **SECRET_KEY** - A secret key used for session storage in the application
  3. **PORT** - The port to use
  4. **IP** - The server IP address

In case you want to run the project locally, you can do so with the following steps:
  1. Clone the project
  2. Install the dependencies from "requirements.txt" (pip install -r requirements.txt)
  3. Create a .env file with the environment variables (see above) to use locally
  4. Type "export FLASK_APP=app.py" in the terminal
  5. Type "flask run" in the terminal

There are no differences between the development and deployed versions of the app.

## Credits

### Content
- Information about companies and stock are taken from [Wikipedia](https://en.wikipedia.org)
- Icons are from [Icons8](https://icons8.com)


## Data model

### user/{userId}
- name: string
- cash: double
- portfolio: object[]
  - stockCode: string
  - quantity: integer
- trades: object[]
  - stockCode: string
  - type: string ('buy' | 'sell')
  - quantity: integer
  - price: double
  - timestamp: date
- valueAtLastTrade: double

### stocks/{stockId}
- stockCode: string
- description: string

### comments/{commentId}
- stockId: string
- content: string
- userId: string
- userName: string
- createdAt: timestamp