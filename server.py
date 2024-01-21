"""View medMinder site."""
from flask import Flask, session, render_template, url_for, request, flash, redirect, jsonify
# Import SQLAlchemy constructor functionn
from flask_sqlalchemy import SQLAlchemy
from model import connect_to_db, db
import crud
import rx_search
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

        # user_id = session.get('user_id')
        # user = crud.get_user_by_id(user_id)

        user = crud.get_user_by_email(email)

        if user and user.password == password:
        # if user.id and user.password == password:
            session['user_id'] = user.user_id
            flash(f"Hello, {user.fname}!")
        return redirect('/profile')

    # If user login attempt fails, display a message asking the user to try logging in again
    else:
        flash('The email or password you entered is incorrect. Please try again.')
    return render_template('homepage.html')


# Route for user to register for account
@app.route('/register', methods=['POST', 'GET'])
def register_user():
    """Register a user."""

    if request.method =='POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user is exists
        existing_user = crud.get_user_by_email('email')

        # If the user is registered but not logged in, redirect the user to login
        if existing_user:
            # Display a message asking the user to login
            flash('A user account already exists with this email. Please log into your account.')
            # Take user to the login form
            return redirect('/login')

        # Add new user to the database
        new_user = crud.add_new_user(fname, lname, email, password)

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

    user_id = (session['user_id'])

    # Pass user id to crud function
    user = crud.get_user_by_id(user_id)

    # Take user to profile page
    return render_template('profile.html', user=user)

# Route for user to add a prescription
@app.route('/add_prescription', methods=['GET','POST'])
def add_prescription():

    if request.method == 'POST':
        # prescription attributes (drugrx name, dosage_amount, frequency_taken)
        drugrx_name = request.form.get('drugrx_name')
        dosage_amount = request.form.get('dosage_amount')
        frequency_taken = request.form.get('frequency_taken')

        # Check if user saved in session
        user_id = session.get('user_id')
        # if the user exists, get user id from database
        existing_user = crud.get_user_by_id(user_id)

        # create new prescrition
        prescription = crud.create_prescription(drugrx_name, dosage_amount, frequency_taken)
        # add new prescrition to db prescriptions
        user.prescriptions.append(prescription)
        # Save db changes
        db.session.commit()
        # Display confirmation that the changes were successful
        flash('New prescription added successfully.')

    # Process request to search Open FDA
    else:
        search_query = request.args.get('search_query')
        if search_query:
            results= rx_search.query_openfda(search_query)
            return render_template('add_prescription.html', results=results)
        return render_template('profile.html')

    # # redirect user to 
    # return redirect('/')

# Add route to handle when user selects a med in js fetch and response function
@app.route('/select_prescription', methods =['POST'])
def select_prescription():

    data = request.json
    brand_name = data.get('brandName')
    generic_name = data.get('genericName')
    unii = data.get('unii')

    # Check if user saved to session
    user_id = session.get('user_id')

    # If user not saved in session, display message asking user to login (dict format)
    if not user_id:
        return jsonify({'Error':'Please try loggin in'})

# Create new prescription for user
# Find a medication in OpenFDA
# Link medication to user


# Route for user to edit a prescription
# @app.route('/edit_prescription', methods='POST')
# def edit_prescription():

    # check if prescription is in db
    # if prescription already exists, redirect to profile page where user can choose a prescription to edit
    # if prescription doesn't exist, display message to user about prescription not existing
    # redirect user to profile page to create a prescription


# View list of all prescriptions
# @app.route('/view_all_prescriptions', methods='POST')
# def get_all_prescriptions():



# If script is main program, initiate and run
if __name__ == "__main__":
    connect_to_db(app) # Establish connection to the database
    app.run(debug=True) # Run Flask app and enable debugging