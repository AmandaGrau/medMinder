"""View medMinder site."""
from flask import Flask, session, render_template, url_for, request, flash, redirect
# Import SQLAlchemy constructor functionn
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.jinja_env.undefined = StrictUndefined


# Creates route to view homepage
@app.route("/")
def home():
    """View homepage."""

    return render_template("home.html")


# Route for user login
@app.route("/login", methods=["POST", "GET"])
def login():
    """Process login for user."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)

    # if user active, save to session
    if user or user.password == password:
        session["user_email"] = user.email
        flash(f"Hello, {user.email}!")
        return redirect("/")

    # if login fails, flash message prompting user to try again
    else:
        flash("The email or password you entered is incorrect. Please try again.")
    return render_template("/home.html")


# Route for user to create account
@app.route("/register", methods=["POST", "GET"])
def register_user():
    """Register a user."""

    if request.method =="POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # if user registered but not logged in, flash a prompt for user to login
        if crud.get_user_by_email(email):
            # flash a message prompting user to login
            flash('Please log in.')
            # redirct user to login form
            return redirect("/login")

        # Create, add, and save new user to database
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()

        # Store user in session and flash message confirming successful login
        session["user_email"] = user.email
        flash(f"Welcome, {user.email}! Thank you for registering with medMinder.")
        # If login successful, redirect to profile page (not yet created)
        return redirect ("/")
    return render_template("register.html")



# Checks if script is main program
# If true, execute following code
if __name__ == "__main__":
    connect_to_db(app) # Establish connection to the database
    app.run(debug=False) # Run Flask app and enable debugging