"""CRUD Operations"""
from model import db, User, Prescription, Medication, connect_to_db

def add_new_user(fname, lname, email, password):
    """Add new user to database."""

    user = User(fname=fname, lname=lname, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return user

# Function to create a new user with email and password
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
def create_prescription(user_id, brand_name, generic_name, unii):
    """Create and return a new prescription"""

    prescription = Prescription(
        user_id=user_id,
        brand_name=brand_name,
        generic_name=generic_name,
        unii=unii
        )

    db.session.add(prescription)
    db.session.commit()

    return prescription

# Function to get prescription by id
def get_prescription_by_id(prescription_id):
    """Returns a prescription by prescription_id."""

    return Prescription.query.get(prescription_id)

# Function to get all prescriptions
def get_all_prescriptions():
    """Return all user prescriptions."""

    return Prescription.query.all()

# Function to get a prescription by drug name
def get_prescription_by_drug_name(brand_name):
    """Return prescription by drug name."""

    return Prescription.query.filter_by(brand_name=brand_name).first()

# Function to get a prescription by dosage_amount
def get_prescription_by_dosage(generic_name):
    """Return prescription by dosage amount."""

    return Prescription.query.filter_by(generic_name=generic_name).first()

# Function to get a prescription by frequency taken
def get_prescription_by_frequency(unii):
    """Return prescription by frequency taken."""

    return Prescription.query.filter_by(unii=unii).first()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)


