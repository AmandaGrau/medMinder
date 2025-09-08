"""CRUD Operations"""
from model import db, User, Prescription, Event, connect_to_db
from datetime import datetime

# Add new user to the database
def add_new_user(fname, lname, email, password, totp_secret=None):
    """Add new user to the database with hashed password."""

    user = User(fname=fname, lname=lname, email=email, totp_secret=totp_secret)
    # Hash the password
    user.set_password(password)
    db.session.add(user)
    return user

# Register a new user with email and password
def register_user(fname, lname, email, password):
    """Create and return a new user with hashed password."""

    user = User(fname=fname, lname=lname, email=email)
    # Hash the password
    user.set_password(password)
    return user

# Function to get all users
def get_all_users():
    """Return all users"""

    return User.query.all()

# Function to get a user by user_id
def get_user_by_id(user_id):
    """Return a user by id."""

    return User.query.get(user_id)

# Function to get user by email
def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email==email).first()

# Function to create a new prescription
def create_prescription(user_id, brand_name, generic_name, strength):
    """Create and return a new prescription"""

    prescription = Prescription(
        user_id=user_id,
        brand_name=brand_name,
        generic_name=generic_name,
        strength=strength)

    db.session.add(prescription)
    db.session.commit()

    return prescription

# Function to delete a prescription
def delete_prescription(user_id, brand_name, generic_name, strength):
    """Delete a prescription"""

    prescription = Prescription(
        user_id=user_id,
        brand_name=brand_name,
        generic_name=generic_name,
        strength=strength)

    db.session.delete(prescription)
    db.session.commit()

    return

# Function to get prescription by id
def get_prescription_by_id(prescription_id):
    """Returns a prescription by prescription_id."""

    return Prescription.query.get(prescription_id)

# Function to get all prescriptions
def get_all_prescriptions():
    """Return all user prescriptions."""

    return Prescription.query.all()

# Function to get a prescription by brand name
def get_prescription_by_brand_name(brand_name):
    """Return prescription by brand name."""

    return Prescription.query.filter_by(brand_name=brand_name).first()

# Function to get a prescription by generic name
def get_prescription_by_generic_name(generic_name):
    """Return prescription by generic name."""

    return Prescription.query.filter_by(generic_name=generic_name).first()

# Function to get a prescription by form taken
def get_prescription_by_strength(strength):
    """Return prescription by strength."""

    return Prescription.query.filter_by(strength=strength).first()

# Function to create a new prescription
def create_event(user_id, title, start, end):
    """Create and return a new event."""

    event = Event(
        user_id=user_id,
        title=title,
        start=start,
        end=end)

    db.session.add(event)
    db.session.commit()

    return event

# Function to delete a prescription
def delete_event(user_id, title, start, end):
    """Delete an event."""

    event = Event(
        user_id=user_id,
        title=title,
        start=start,
        end=end)

    db.session.delete(event)
    db.session.commit()

    return

# Function to get prescription by id
def get_event_by_id(event_id):
    """Return event by event id."""

    return Event.query.get(event_id)

# Function to get all prescriptions
def get_all_events(user_id):
    """Return all events for user."""

    return Event.query.all(user_id)

# Function to get a prescription by brand name
def get_event_by_title(title):
    """Return an event by title."""

    return Event.query.filter_by(title=title).first()

# Function to get a prescription by generic name
def get_event_by_start(start):
    """Return an event by start date."""

    return Event.query.filter_by(start=start).first()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)