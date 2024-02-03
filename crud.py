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

# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCTIONS TO HANDLE CALENDAR EVENTS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# # Create a new calendar event
# def create_event(user_id, event_title, event_start, event_end, event_url, recurrence_pattern, recurrence_interval, recurrence_days_of_week, recurrence_day_of_month, recurrence_week_and_day, end_date_for_recurrence):
#     """Create and return new calendar event"""

#     event = RefillEvent(
#         user_id=user_id,
#         event_title=event_title,
#         event_start=event_start,
#         event_end=event_end,
#         event_url=event_url,
#         # Daily, Weekly, Monthly, Yearly, Custom
#         recurrence_pattern=recurrence_pattern,
#         # Custom pattern input (every _ days, etc.)
#         recurrence_interval=recurrence_interval,
#         # Weekly reccurence on a given day
#         recurrence_days_of_week=recurrence_days_of_week,
#         # For monthly recurrence on a given day
#         recurrence_day_of_month=recurrence_day_of_month,
#         # For monthly recurrence on given week and day
#         recurrence_week_and_day=recurrence_week_and_day,
#         # End date for recurring events
#         end_date_for_recurrence=end_date_for_recurrence
#     )

#     db.session.add(event)
#     db.session.commit()

#     return event

# # Get events by user id
# def get_events_by_user(user_id):
#     """Return all of a user's calendar events"""

#     return RefillEvent.query.filter_by(user_id=user_id).all()

# # Get event by event id
# def get_event_by_id(event_id):
#     """Return event by id"""


# # Update existing event
# def update_event(event_id, event_title, event_start, event_end, event_url, recurrence_pattern, recurrence_interval, recurrence_days_of_week, recurrence_day_of_month, recurrence_week_and_day, end_date_for_recurrence):
    
#     event = RefillEvent.query.get(event_id)
#     event.event_title=event_title,
#     event.event_start=event_start,
#     event.event_end=event_end,
#     event.event_url=event_url,
#     # Daily, Weekly, Monthly, Yearly, Custom
#     event.recurrence_pattern=recurrence_pattern,
#     # Custom pattern input (every _ days, etc.)
#     event.recurrence_interval=recurrence_interval,
#     # Weekly reccurence on a given day
#     event.recurrence_days_of_week=recurrence_days_of_week,
#     # For monthly recurrence on a given day
#     event.recurrence_day_of_month=recurrence_day_of_month,
#     # For monthly recurrence on given week and day
#     event.recurrence_week_and_day=recurrence_week_and_day,
#     # End date for recurring events
#     event.end_date_for_recurrence=end_date_for_recurrence
    
#     db.session.commit()

# # Delete a calendar event
# def delete_event(event_id):
#     """Delete calendar event by event id"""

#     event = RefillEvent.query.get(event_id)

#     db.session.delete(event)
#     db.session.commit()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
