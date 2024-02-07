"""View site."""
from flask import Flask, session, render_template, url_for, request, flash, redirect, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from model import db, connect_to_db, Event
import crud
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.jinja_env.undefined = StrictUndefined

# >>>>>>>>>>>> CALENDAR VIEW & EVENT HANDLING <<<<<<<<<<<<<<<

@app.route('/calendar')
def view_calendar():

    return render_template('calendar.html')



@app.route('/add-event', methods=['POST'])
def add_event():
    data = request.get_json()
    
    user_id = session.get('user_id')  # Make sure the user is logged in
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 403
    
    title = data['title']
    start_date = datetime.strptime(data['start'], '%Y-%m-%d')
    end_date = datetime.strptime(data['end'], '%Y-%m-%d')

    # Create and save the event to the database
    new_event = Event(user_id=user_id, title=title, start=start_date, end=end_date)
    db.session.add(new_event)
    db.session.commit()

    return jsonify({'message': 'Event added successfully', 'event_id': new_event.event_id})

@app.route('/fetch-events')
def fetch_events():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Please log in.'}), 403

    events = Event.query.filter_by(user_id=user_id).all()
    return jsonify([event.serialize() for event in events])

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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

        user = crud.get_user_by_email(email)

        if user and user.password == password:
        # if user.id and user.password == password:
            session['user_id'] = user.user_id
            flash(f"Hello, {user.fname}!")
        return redirect('/profile')

    # If login fails, display a message asking the user to try logging in again
    else:
        flash('The email or password you entered is incorrect. Please try again.')
    return render_template('homepage.html')

# Route for user logout
@app.route('/logout')
def user_logout():
    session.clear()
    flash('Logout Complete')
    return redirect('/')

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

        # If user is registered but not logged in, redirect user to login
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
        flash(f'Welcome, {fname}! Thank you for registering.')
        # If login successful, redirect to profile page
        return redirect ('/profile')

    return render_template('register.html')

# Route to view profile
@app.route('/profile', methods=['GET'])
def view_profile():
    """View user profile."""

    user_id = session.get('user_id')
    existing_user = crud.get_user_by_id(user_id)

    #Initializeempty list for user prescriptions
    user_prescriptions = []

    if existing_user:
        # Retrieve User's prescriptions
        user_prescriptions = existing_user.prescriptions

    else:
        flash('Error viewing prescriptions!')
    return render_template('profile.html', user=existing_user, prescriptions=user_prescriptions)

# Add a prescription
@app.route('/profile', methods =['POST'])
def add_prescription():

    # Get data and extract brand name, generic name, and unii
    med_result_data = request.json
    brand_name = med_result_data.get('brandName')
    generic_name = med_result_data.get('genericName')
    strength = med_result_data.get('strength')
    # dosage_form = med_result_data.get('dosageForm')
    # unii = med_result_data.get('unii')

    # Check if user in session
    user_id = session.get('user_id')
    # If user logged in, get user from the database
    if user_id:
        user = crud.get_user_by_id(user_id)

        # Add a new prescription which is linked to medication and user
        prescription = crud.create_prescription(user_id, brand_name, generic_name, strength)
        user.prescriptions.append(prescription)
        db.session.add(user)
        db.session.commit()

        # Return JSON response confirming prescription added
        return jsonify({'brandName': brand_name, 'message':'New prescription added successfully'})
    # If user not logged in:
    return jsonify({'Error':'Please login'})


# Delete a prescription
@app.route('/profile/delete_prescription', methods=['POST'])
def delete_prescription():

    med_result_data = request.json
    prescription_id = med_result_data.get('prescriptionId')

    # Check if user in session
    user_id = session.get('user_id')
    # If user, get user details from database
    if user_id:
        user = crud.get_user_by_id(user_id)

        # Delete prescription from database
        prescription = crud.get_prescription_by_id(prescription_id)
        if prescription:
            db.session.delete(prescription)
            db.session.commit()

            return jsonify({'message':'Prescription has been deleted.'})

        else:
            return jsonify({'Error': 'Prescription not found.'})

    return jsonify({'Error':'Please login'})

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=5000)