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

## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

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