"""CRUD Operations"""

from model import db, User, Prescription, Medication, connect_to_db

# Function to create a new user with email and password
def register_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


# Function to get all usersujj
def get_all_users():
    """Return all users"""

    return User.query.all()


# Function to get a user by user_id
def get_user_by_id(user_id):
    """Return a user by user id."""

    return User.query.get(user_id)


# Function to get user by email
def get_user_by_email(email):
    """Return a user by email."""

    return User.query.get(email)


# Function to create a new prescription
def create_prescription(drug_name, dosage_amount, frequency_taken):
    """Create and return a new prescription"""

    prescription = Prescription(
        drug_name=drug_name,
        dosage_amount=dosage_amount,
        frequency_taken=frequency_taken
        )

    return prescription


# Function to get all prescriptions
def get_all_prescriptions():
    """Returns all user prescriptions."""

    return Prescription.query.all()


# Function to get a prescription by drug name
def get_prescription_by_drug_name(drug_name):
    """Return a prescription by drug name."""

    return Prescription.query.get(drug_name)


# Function to get a prescription by dosage_amount
def get_prescription_by_dosage(dosage_amount):
    """Return a prescription by dosage amount."""

    return Prescription.query.get(dosage_amount)


# Function to get a prescription by frequency taken
def get_prescription_by_frequency(frequency_taken):
    """Return a prescription by frequency taken."""

    return Prescription.query.get(frequency_taken)


# Function to get all (API) meds




# Sprint 2.0
# function to create new doctor
# function to get doctor by id
# function to get doctor by name






if __name__ == "__main__":
    from server import app
    connect_to_db(app)


