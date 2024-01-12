"""View medMinder site."""


from flask import Flask, session, render_template, request, flash, redirect
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)

import os

app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined



# ---------
# To Do:
# ---------
# Create flask session
# Create routes / view functions
# return redirect or render template for each route
# Create route for user to view their prescriptions
# Create route for prescription updates 
# Create route for user to view their treating doctors
# Create route to handle doctor updates


# Create route to homepage
@app.route("/")
def homepage():
    """View medMinder homepage."""

    return render_template("homepage.html")


# Create route for user login
# @app.route("login")
# def user_login():
#     """Process login for user."""



# user will log in using email and password
# assign a variable to create a session with user email
# if user not logged in, flash a prompt for user to login

#     pass


# Check if script is main program
# If true, execute following code
if __name__ == "__main__":
    connect_to_db(app) # Establish connection to the database
    app.run(host="0.0.0.0", port=5000, debug=False) # Run Flask app and enable debugging