"""Models for prescription tracking app."""
from datetime import datetime
from flask import Flask, session, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///prescriptions", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{'prescriptions'}"
    flask_app.config["SQLALCHEMY_ECHO"] = True
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    print("Connected to db!")


class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    prescriptions = db.relationship("Prescription", back_populates="user")
    refillevents= db.relationship("RefillEvent", back_populates="user")

    def __repr__(self):
        """Show user details."""
        return f"<First:{self.fname} Last:{self.lname} Email:{self.email} Password:{self.password}>"


# User's prescribed medications
class Prescription(db.Model):
    """The user's prescribed medication."""

    __tablename__ = "prescriptions"

    prescription_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.medication_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    brand_name = db.Column(db.String)
    generic_name = db.Column(db.String)
    strength = db.Column(db.String)

    user = db.relationship("User", back_populates="prescriptions")
    medication = db.relationship("Medication", back_populates="prescriptions")

    # Foreign keys argument and primary join
    refillevents = db.relationship("RefillEvent", back_populates="prescription")

    def __repr__(self):
        """Show prescribed dosge, frequency taken, and refill due date."""
        return f"<Brand:{self.brand_name} Generic:{self.generic_name} Strength:{self.strength}>"


# A calendar for prescription refill dates and reminders
class RefillEvent(db.Model):
    """Prescription refill events and reminders"""

    __tablename__ = "refillevents"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    prescription_id = db.Column(db.Integer, db.ForeignKey("prescriptions.prescription_id"))
    event_title = db.Column(db.String(255), nullable=False)
    event_start = db.Column(db.DateTime, nullable=False)
    event_end = db.Column(db.DateTime, nullable=False)
    event_url = db.Column(db.String(255))
    # Daily, Weekly, Monthly, Yearly, Custom
    recurrence_pattern = db.Column(db.String(20))
    # Custom pattern input (every _ days, etc.)
    recurrence_interval = db.Column(db.Integer)
    # Weekly reccurence on a given day
    recurrence_days_of_week = db.Column(db.String(7))
    # For monthly recurrence on a given day
    recurrence_day_of_month = db.Column(db.Integer)
    # For monthly recurrence on given week and day
    recurrence_week_and_day = db.Column(db.String(20))
    # End date for recurring events
    end_date_for_recurrence = db.Column(db.DateTime)


    user = db.relationship("User", back_populates="refillevents")

    # Foreign keys argument and primary join
    prescription = db.relationship("Prescription", back_populates="refillevents", foreign_keys=[prescription_id], remote_side=[Prescription.prescription_id])

    def __repr__(self):
        """Show refill event details"""
        return f"<Event:{self.event_title}, Start:{self.event_start} End:{self.event_end}>"


# Medications queried from Open FDA
class Medication(db.Model):
    """A medication."""

    __tablename__ = "medications"

    medication_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String)
    generic_name = db.Column(db.String)
    strength = db.Column(db.String)

    prescriptions = db.relationship("Prescription", back_populates="medication")

    def __repr__(self):
        """Medication names and strengths."""
        return f"<Brand:{self.brand_name}, Generic:{self.generic_name} Strength:{self.strength}>"

if __name__ == "__main__":
    from server import app
    # Function call connecting the app to database
    connect_to_db(app)