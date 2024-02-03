"""View site."""
from flask import Flask, session, render_template, url_for, request, flash, redirect, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from model import db, connect_to_db, RefillEvent
import crud
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

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Calendar View <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Route to view calendar
@app.route('/calendar')
def calendar():
    """View Calendar"""

    # Get user from session
    user_id = session.get('user_id')
    if user_id:
        events = crud.get_events_by_user(user_id)
        return render_template('calendar.html', events=events)
    else:
        flash('Please log in to view the calendar.')
        return redirect(url_for('login'))

    # events = crud.get_events_by_user(session.get('user_id'))
    # return redirect(url_for('calendar'))
    

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Handle events from form <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Route to handle calendar events
@app.route('/calendar/add_event', methods=["POST"])
def add_event():
    """Process calendar event from user input"""

    # Get user from session
    user_id = session.get('user_id')

    # Get user event input from the form submission
    event_title = request.form.get('event_title')
    event_start = request.form.get('event_start')
    event_end = request.form.get('event_end')
    event_url = request.form.get('event_url')
    # Daily, Weekly, Monthly, Yearly, Custom
    recurrence_pattern = request.form.get('recurrence_pattern')
    # Custom pattern input (every _ days, etc.)
    recurrence_interval = request.form.get('recurrence_interval')
    # Weekly reccurence on a given day
    recurrence_days_of_week = request.form.get('recurrence_days_of_week')
    # For monthly recurrence on a given day
    recurrence_day_of_month = request.form.get('recurrence_day_of_month')
    # For monthly recurrence on given week and day
    recurrence_week_and_day = request.form.get('recurrence_week_and_day')
    # End date for recurring events
    end_date_for_recurrence = request.form.get('end_date_for_recurrence')

    # Create new event
    crud.create_event(user_id, event_title, event_start, event_end, event_url, recurrence_pattern, recurrence_interval, recurrence_days_of_week, recurrence_day_of_month, recurrence_week_and_day, end_date_for_recurrence)

    db.session.commit()

    flash('Event added successfully')
    return redirect(url_for('calendar'))


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Get event from database <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/calendar/get_events', methods=['GET'])
def get_events():

    # Get user from session
    user_id=session['user_id']

    # Get events by user id
    events = RefillEvent.query.filter_by(user_id=user_id).all()
    
    # Convert events to list of dict for JSON
    event_list = []

    # Loop over events and append to events list
    for event in events:
        event_data = {
            'event_title': event.event_title,
            'event_start': event.event_start.strftime('%Y-%m-%dT%H:%M:%S'),
            'event_end': event.event_end.strftime('%Y-%m-%dT%H:%M:%S'),
            'event_url': event.event_url,
            # Daily, Weekly, Monthly, Yearly, Custom
            'recurrence_pattern': event.recurrence_pattern,
            # Custom pattern input (every _ days, etc.)
            'recurrence_interval': event.recurrence_interval,
            # Weekly reccurence on a given day
            'recurrence_days_of_week': event.recurrence_days_of_week,
            # For monthly recurrence on a given day
            'recurrence_day_of_month': event.recurrence_day_of_month,
            # For monthly recurrence on given week and day
            'recurrence_week_and_day': event.recurrence_week_and_day,
            # End date for recurring events
            'end_date_for_recurrence': event.end_date_for_recurrence
        }
        event_list.append(event_data)
    return jsonify({'events':event_list})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Update Event <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/calendar/edit_event/<int:event_id>', methods=['POST'])
def edit_event(event_id):

    # Get user from session
    user_id = session['user_id']
    # If user, get user details from database
    if user_id:
        user = crud.get_user_by_id(user_id)

    event = RefillEvent.query.get(event_id)

    # Update event properties from form submission
    event.event_title = request.form.get('event_title')
    event.event_start = request.form.get('event_start')
    event.event_end = request.form.get('event_end')
    event.event_url = request.form.get('event_url')
    # Daily, Weekly, Monthly, Yearly, Custom
    event.recurrence_pattern = request.form.get('recurrence_pattern')
    # Custom pattern input (every _ days, etc.)
    event.recurrence_interval = request.form.get('recurrence_interval')
    # Weekly reccurence on a given day
    event.recurrence_days_of_week = request.form.get('recurrence_days_of_week')
    # For monthly recurrence on a given day
    event.recurrence_day_of_month = request.form.get('recurrence_day_of_month')
    # For monthly recurrence on given week and day
    event.recurrence_week_and_day = request.form.get('recurrence_week_and_day')
    # End date for recurring events
    event.end_date_for_recurrence = request.form.get('end_date_for_recurrence')

    db.session.commit()

    return jsonify({'message':'Event updated successfully'})

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Delete Event <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/calendar/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):

    event = RefillEvent.query.get(event_id)

    db.session.delete(event)
    db.session.commit()

    return jsonify({'message':'Event deleted successfully'})


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=5000)


# # Save changes made to prescriptions in dropdown menus
# @app.route('/profile/save_changes', methods=['POST'])
# def save_prescription_changes():

#     med_result_data = request.json
#     prescription_id = med_result_data.get('prescriptionId')

#     # Check if user in session
#     user_id = session.get('user_id')
#     # If user, get user details from database
#     if user_id:
#         user = crud.get_user_by_id(user_id)

#         # Delete prescription from database
#         prescription = crud.get_prescription_by_id(prescription_id)
#         if prescription:
#             db.session.add(prescription)
#             db.session.commit()

#             return jsonify({'message':'Updates saved successfully!'})

#         else:
#             return jsonify({'Error': 'Prescription not found.'})

#     return jsonify({'Error':'Please login'})



