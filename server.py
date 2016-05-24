"""Stocks"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import json

from model import Stock, connect_to_db, db
# need to import Tweet table as part of phase 2


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/stock-detail")
def stock_detail():
    """Show stock details"""
    ticker = request.args.get("ticker")
    session['ticker'] = ticker
    print "In our session is " + session['ticker']
    current_stock = Stock.query.get(ticker)
    spx_member = Stock.query.filter_by(ticker="ticker").first()

    #Provide feedback to user on whether if ticker is valid

    if current_stock is None:
        flash("Please enter a valid ticker symbol")
        return render_template("homepage.html")

    quotes = current_stock.get_quotes()
    tweets = current_stock.get_tweets()

    return render_template("stock-detail.html",
                           stock=current_stock,
                           quotes=quotes, tweets=tweets)


@app.route("/data.json")
def get_bar_data():
    """Send stock volume data to bar chart"""
    print "In our JSON route" + session.get("ticker")
    ticker = session.get("ticker")
    current_stock = Stock.query.get(ticker)
    quotes = current_stock.get_quotes()
    # print "****************************"
    # print quotes
    # print "****************************"

    # datetime = quotes.Timestamp
    # volume = quotes.volume

    answer = []

    for i in range(len(quotes)):
        answer.append({'date': quotes[i]['Timestamp'], 'value': quotes[i]['volume']})
        print "The timestamp should be: " + quotes[i]['Timestamp']
    return json.dumps(answer)

# @app.route("/spx-member")
# def is_spx_member():
#     """Provide feedback to user on whether if ticker is valid"""


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
