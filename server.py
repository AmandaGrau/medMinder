"""View medMinder site."""
from flask import Flask, session, render_template, url_for, request, flash, redirect
# Import SQLAlchemy constructor functionn
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.jinja_env.undefined = StrictUndefined


# Creates route to view homepage
@app.route("/")
def home():
    """View homepage."""

    return render_template("homepage.html")


# Route for user login
@app.route("/login", methods=["POST", "GET"])
def login():
    """Process login for user."""

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = crud.get_user_by_id('user_id')
        if user.id and user.password == password:
            session["user_id"] = user.user_id
            # # save name to session
            # session['user.fname'] = user.fname
            # flash message that greets user with first name
            flash(f"Hello, {user.fname}!")
        return redirect('/profile')

    # if login fails, flash message prompting user to try again
    else:
        flash('The email or password you entered is incorrect. Please try again.')
    return render_template('homepage.html')


# Route for user to create account
@app.route('/register', methods=['POST', 'GET'])
def register_user():
    """Register a user."""

    if request.method =='POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Need to check if user is an existing user
        existing_user = crud.get_user_by_email('email')

        # if user is registered but not logged in
        if existing_user:
            # Display a message prompting the user to login
            flash('A user account already exists with this email. Please log into your account.')
            # Take user to the login form
            return redirect('/login')

        # Create and add the new user to the database
        new_user = crud.add_new_user(fname, lname, email, password)
        # db.session.commit()

        # Save user to session
        session['user_id'] = new_user.user_id
        # Display message confirming successful login
        flash(f'Welcome, {fname}! Thank you for registering with medMinder.')
        # If login successful, redirect to profile page (not yet created)
        return redirect ('/profile')

    return render_template('register.html')

# Route for user to view profile
@app.route('/profile')
def view_profile():
    """View user profile."""

    if 'user_id' not in session:
        flash(f'Please log in to view your profile.')
        return redirect('/login')
    #  Get the user id from the session
    user_id = (session['user_id'])
    # pass user id from session to crud function
    user = crud.get_user_by_id(user_id)
    return render_template('profile.html', user=user)
    # return render_template("profile.html")

@app.route('/add_prescription', methods=['POST'])
def add_prescription():

    # prescription attributes (drugrx name, dosage_amount, frequency_taken)
    drugrx_name = request.form.get('drugrx_name')
    dosage_amount = request.form.get('dosage_amount')
    frequency_taken = request.form.get('frequency_taken')

    # Check if user saved in session
    user = session.get('user_id')
    # if the user exists, get user id from database
    existing_user = crud.get_user_by_id('user_id')

    # if user exists:
    if existing_user:
        # create new prescrition
        prescription = crud.create_prescription(drugrx_name, dosage_amount, frequency_taken)
        # add new prescrition to db prescriptions
        user.prescriptions.append(prescription)
        # Save db changes
        db.session.commit()
        # Display confirmation that the changes were successful
        flash('New prescription had been added successfully.')

    # if the user doesn't exist, display a message to prompt user to login or register
    else:
        flash('Please login or register to manage prescriptions.')
    # redirect user to login
    return redirect('/')

# Edit a prescription
# @app.route('/edit_prescription', methods='POST')
# def edit_prescription():

    # check if prescription is in db
    # if prescription already exists, redirect to profile page where user can choose a prescription to edit
    # if prescription doesn't exist, display message to user about prescription not existing
    # redirect user to profile page to create a prescription


# View list of all prescriptions
# @app.route('/view_all_prescriptions', methods='POST')
# def get_all_prescriptions():



# If script is main program, initiate app and run code
if __name__ == "__main__":
    connect_to_db(app) # Establish connection to the database
    app.run(debug=True) # Run Flask app and enable debugging