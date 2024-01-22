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

    # Take user to the profile page
    return render_template('profile.html', user=user)

# Route for user to add a prescription
@app.route('/add_prescription', methods=['GET','POST'])
def add_prescription():

    if request.method == 'POST':
        # Test revisions to properly display query results to profile page
        # if 'brandName' in request.form and 'genericName' in request.form and 'unii' in request.form:
        #     brand_name = request.form['brandName']
        #     generic_name = request.form['genericName']
        #     unii = request.form['unii']

        # prescription attributes (drugrx name, dosage_amount, frequency_taken)
        drugrx_name = request.form.get('drugrx_name')
        dosage_amount = request.form.get('dosage_amount')
        frequency_taken = request.form.get('frequency_taken')

        # Check if user saved in session
        user_id = session.get('user_id')
        # if the user exists, get user id from database
        existing_user = crud.get_user_by_id(user_id)

        # Check if user exists
        if existing_user:
            # create new prescrition and add to user's profile
            prescription = crud.create_prescription(drugrx_name, dosage_amount, frequency_taken)
            existing_user.prescriptions.append(prescription)
            # Save db changes
            db.session.commit()
            # Display confirmation prescription was added
            flash('New prescription added successfully.')
            # redirect to updated profile
            return redirect('profile')

        # If user doesn't exist
        else:
            # Display alert message
            flash('Sorry, user not found.')
            # dedirect user to login or register

    # Handle search request to Open FDA
    else:
        search_query = request.args.get('search_query')
        if search_query:
            results= rx_search.query_openfda(search_query)
            # Render add_prescription template for POST request
            return render_template('add_prescription.html', results=results)

        # Render the same page for GET request without a query
        return render_template('add_prescription.html')
    
    # Default page to be rendered for add_prescription route
    return render_template('add_prescription.html')


# Add a route to display query results in the user profile
@app.route('/profile')
def display_to_profile():
    user_id = session.get('user_id')
    existing_user = crud.get_user_by_id(user_id)

    if existing_user:
        # Retrieve User's prescriptions
        user_prescriptions = existing_user.prescriptions
        return render_template('profile.html', user=existing_user, presciptions=user_prescriptions)

    else:
        flash('Please register or login to manage prescriptions')


# Route to handle user selecting a med
@app.route('/select_prescription', methods =['POST'])
def select_prescription():

    # Get data with POST request and extract brand name, generic name, and unii
    data = request.json
    brand_name = data.get('brandName')
    generic_name = data.get('genericName')
    unii = data.get('unii')

    # Check if user logged in session
    user_id = session.get('user_id')
    # If user logged in, get user from the database
    if user_id:
        user = crud.get_user_by_id(user_id)

    # If user not saved in session, display message asking user to login (dict format)
    # if not user_id:
        # return jsonify({'Error':'Please try logging in'})

    # Query database with unqiue code to determine if a medication already exists
    # medication = Medication.query.filter_by(unii=unii).first()

    # # If med doesn't exist, create and add med to the database
    # if not medication:
    #     medication = Medication(brand_name=brand_name, generic_name=generic_name, unii=unii)
    #     db.session.add(medication)
    #     db.session.commit()

    # Create and add a new prescription, linking it to the newly added medication and to the user
        prescription = crud.create_prescription(brand_name, generic_name, unii)
        user.prescriptions.append(prescription)
        db.session.commit()

        # Return JSON response confirming prescription being added
        return jsonify({'brandName': brand_name, 'message':'New prescription added successfully'})

    # If user not logged in:
    return jsonify({'Error':'Please try logging in'})

# Add route for user to edit a prescription
# @app.route('/edit_prescription', methods='POST')
# def edit_prescription():

    # check if prescription is in db
    # if prescription already exists...
    # redirect to prescriptions list where user can choose and edit a prescription
    # if prescription doesn't exist, display 'not found' message to user
    # redirect user to add a prescription


# Add route for user to view all prescriptions
# @app.route('/view_all_prescriptions', methods='POST')
# def get_all_prescriptions():



# If script is main program, initiate and run
if __name__ == "__main__":
    connect_to_db(app) # Establish connection to the database
    app.run(debug=True) # Run Flask app and enable debugging