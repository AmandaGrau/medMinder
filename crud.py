"""CRUD Operations"""
from model import db, User, Prescription, Medication, connect_to_db

# Add a new registered user to the database
def add_new_user(fname, lname, email, password):
    """Add new user to database."""

    user = User(fname=fname, lname=lname, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return user

# Register a new user with email and password
def register_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname, lname=lname, email=email, password=password)

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

    return User.query.filter_by(email=email).first()

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


# Functions to handle calendar and events


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
