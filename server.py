from flask import Flask, session, render_template, url_for, request, flash, redirect, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from model import db, connect_to_db, Event
import crud
import os

# Imports for 2FA
import pyotp
import qrcode
import io
import base64

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Raise errors for undefined template variables
app.jinja_env.undefined = StrictUndefined

# =====  USER LOG IN  ===== #
@app.route('/')
def home():
    """Display the homepage page."""
    return render_template('home.html')

# =====  REGISTRATION  ===== #
@app.route('/register', methods=['POST', 'GET'])
def register_user():
    """Handle user registration with GET and POST methods."""
    
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        # Extract registration data from the form
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Generate TOTP secret
        totp_secret = pyotp.random_base32()

        # Check if user already exists with this email
        existing_user = crud.get_user_by_email(email)
        if existing_user:
            # User already registered - redirect to login  
            flash('A user account already exists with this email. Please log into your account.')          
            return redirect('/login')

        # Create new user account
        user = crud.add_new_user(fname, lname, email, password, totp_secret)
        db.session.commit()
        
        # Generate QR code - FIXED TYPO HERE
        totp_uri = pyotp.TOTP(totp_secret).provisioning_uri(name=email, issuer_name='medMinder')    
        img = qrcode.make(totp_uri)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # Show the QR code to the user for 2FA setup
        return render_template('2FA_setup.html', qr_b64=qr_b64, totp_secret=totp_secret, email=email)
    
# =====  QR CODE VERIFICATION  ===== #
@app.route('/2FA_setup', methods=['POST'])
def setup_2FA():
    """Handle 2FA setup verification after registration."""
    code = request.form.get('code')
    email = request.form.get('email')
    user = crud.get_user_by_email(email)
    
    if user and user.totp_secret:
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(code):
            # Log in the user
            session['user_id'] = user.user_id  
            flash('Registration and 2FA setup complete! You are now logged in.', 'success')
            return redirect('/profile')
    
    flash('Invalid code. Please try again.', 'danger')
    
    # Re-generate QR code for retry
    totp_uri = pyotp.TOTP(user.totp_secret).provisioning_uri(name=email, issuer_name='medMinder')    
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    qr_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return render_template('2FA_setup.html', qr_b64=qr_b64, totp_secret=user.totp_secret, email=email)

# =====  LOGIN AUTH CODE ===== #
@app.route('/2FA_login', methods=['POST'])
def login_2FA():
    """Handle 2FA verification during login."""
    code = request.form.get('code')
    email = request.form.get('email')
    user = crud.get_user_by_email(email)
    
    if user and user.totp_secret:
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(code):
            session['user_id'] = user.user_id
            # Clear the pre-2FA session data
            session.pop('pre_2fa_user_id', None)
            flash('Login successful!', 'success')
            return redirect('/profile')
    
    flash('Invalid 2FA code. Please try again.', 'danger')
    return render_template('2FA_login.html', email=email)

# =====  USER LOG IN  ===== #
@app.route('/login', methods=['POST', 'GET'])
def login():
    '''Log in a user.'''

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        # Extract login credentials from the form
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Retrieve user from the database by email
        user = crud.get_user_by_email(email)
        
        # Verify the user exists and password hash matches
        if user and user.check_password(password):
            # Store temporary session data for 2FA verification
            session['pre_2fa_user_id'] = user.user_id
            return render_template('2FA_login.html', email=email)
        else:
            # Flash message: user login failed - invalid credentials 
            flash('Invalid credentials have been entered. Please try again.', 'danger')
            return render_template('login.html')
        
# =====  USER LOG OUT  ===== #
@app.route('/logout')
def user_logout():
    """Log out current user by clearing the session."""
    
    session.clear()  # Remove all session data
    flash('Logout Complete', 'success')
    return redirect('/')

# =====  VIEW PROFILE  ===== #
@app.route('/profile', methods=['GET'])
def view_profile():
    """Display user profile page with prescription details."""
    
    # Get the current user from session
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your profile.', 'warning')
        return redirect('/login')
        
    existing_user = crud.get_user_by_id(user_id)

    # Initialize empty list for prescriptions
    user_prescriptions = []

    if existing_user:
        # Retrieve all prescriptions for current user
        user_prescriptions = existing_user.prescriptions
    else:
        flash('Error viewing prescriptions!', "danger")
        
    return render_template('profile.html', user=existing_user, prescriptions=user_prescriptions)

# =====  ADD PRESCRIPTION  ===== #
@app.route('/profile', methods=['POST'])
def add_prescription():
    """Add a prescription for the current user."""
    
    # Extract brand name, generic name, strength
    med_result_data = request.json
    brand_name = med_result_data.get('brandName')
    generic_name = med_result_data.get('genericName')
    strength = med_result_data.get('strength')
    
    # Verify user is logged in
    user_id = session.get('user_id')
    if user_id:
        user = crud.get_user_by_id(user_id)

        # Create new prescription and associate with the user
        prescription = crud.create_prescription(user_id, brand_name, generic_name, strength)
        user.prescriptions.append(prescription)
        db.session.add(user)
        db.session.commit()

        # Return success response with prescription details
        return jsonify({
            'brandName': brand_name, 
            'message': 'New prescription added successfully', 
            'prescription_id': prescription.prescription_id
        })
    
    # User not authenticated - not logged in
    return jsonify({'error': 'Please login'}), 401

# ======  DELETE PRESCRIPTION  ===== #
@app.route('/delete-prescription/<int:prescription_id>', methods=['DELETE'])
def delete_prescription(prescription_id):
    """Delete a prescription for the current user"""
    
    try:
        # Check if user is logged in
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Authentication required'               
            }), 401
            
        # Find user's prescription
        prescription = crud.get_prescription_by_id(prescription_id)

        if not prescription:
            return jsonify({
                'success': False, 
                'error': 'Prescription not found'
            }), 404
                
        # Security check: ensure user owns this prescription
        if prescription.user_id != user_id:
            return jsonify({
                'success': False, 
                'error': 'Unauthorized access'
            }), 403        
                
        db.session.delete(prescription)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prescription deleted successfully.'
        }), 200
        
    except Exception as e:
        # Log error for debugging
        print(f"Error deleting prescription {prescription_id}: {str(e)}")

        db.session.rollback()
        
        return jsonify({
            'success': False,
            'error': 'Server error occurred'
        }), 500

# =====  VIEW CALENDAR PAGE  ===== #
@app.route('/calendar')
def view_calendar():
    """Display the calendar page for the user."""    
    
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in to view your calendar.', 'warning')
        return redirect('/login')
        
    return render_template('calendar.html')

# =====  ADD CALENDAR EVENT  ===== #
@app.route('/add-event', methods=['POST'])
def add_event():
    """Add a new calendar event."""
        
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Please log in to manage events.'}), 401
            
        # Get json data from request    
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        if not data.get('title') or not data.get('start'):
            return jsonify({'success': False, 'error': 'Event title and start date are required.'}), 400

        new_event = Event(
            title = data['title'],
            start = data['start'],
            end = data.get('end', data['start']),
            all_day = data.get('allDay', True),
            user_id = session['user_id']
        )        
        
        db.session.add(new_event)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Event added successfully',
            'event': {
                'id': new_event.event_id,
                'title': new_event.title,
                'start': new_event.start,
                'end': new_event.end,
                'allDay': new_event.all_day                
            }
        })

    except Exception as e:
        db.session.rollback()
        print(f"Error adding event: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500
    
# =====  DELETE CALENDAR EVENT  ===== #
@app.route('/delete-event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Delete calendar event for the current user."""
    
    try:
        # Check is user is logged in
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Please log in to manage events.'}), 401

        event = Event.query.filter(
            Event.event_id == event_id,
            Event.user_id == session['user_id']  # Ensure user owns event
        ).first()
        
        if not event:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        
        # Delete event
        db.session.delete(event)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Event deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting event: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500
        
# =====  UPDATE CALENDAR EVENT  ===== #
@app.route('/update-event/<int:event_id>', methods=['PUT'])
def update_event(event_id):   
    """Update calendar event for the current user."""
    
    try:
        # Check is user is logged in
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Please log in to manage events.'}), 401

        data = request.get_json()

        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        if not data.get('title') or not data.get('start'):
            return jsonify({'success': False, 'error': 'Event title and start date are required'}), 400
        
        event = Event.query.filter(
            Event.event_id == event_id,
            Event.user_id == session['user_id']  # Ensure user owns event
        ).first()
        
        if not event:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        
        # Update event fields
        event.title = data['title']
        event.start = data['start']
        event.end = data.get('end', data['start'])
        event.all_day = data.get('allDay', True)
    
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Event updated successfully',
            'event': {
                'id': event.event_id,
                'title': event.title,
                'start': event.start,
                'end': event.end,
                'allDay': event.all_day                
            }
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Error updating event: {str(e)}")
        return jsonify({'success': False, 'error': 'Server error'}), 500    

# =====  FETCH CALENDAR EVENT  ===== #
@app.route('/fetch-events')
def fetch_events():
    """Fetch all calendar events for the logged-in user."""
    
    try:
        # check if user is logged in
        if 'user_id' not in session:
            return jsonify({'error': 'Please log in.'}), 401

        # Fetch user's events
        events = Event.query.filter(Event.user_id == session['user_id']).all()
        
        # Format events for FullCalendar
        formatted_events = []
        for event in events:
            formatted_events.append({
                'id': str(event.event_id), 
                'title': event.title,
                'start': event.start,
                'end': event.end,
                'allDay': event.all_day  
            })

        return jsonify(formatted_events)
    
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify([])    
        

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug=True, port=5000)