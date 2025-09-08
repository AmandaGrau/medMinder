"""Models for prescription tracking app."""

from datetime import datetime
from flask import Flask, session, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///prescriptions", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
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
    password = db.Column(db.String(255), nullable=False)
    totp_secret = db.Column(db.String(32), nullable=True)

    prescriptions = db.relationship("Prescription", back_populates="user")
    events = db.relationship("Event", back_populates="user")
    
    def set_password(self, password):
        """Hash and set the Users' password."""
        
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if provided password matches the hashed password."""
    
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f"<First:{self.fname} Last:{self.lname} Email:{self.email}>"


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

    def __repr__(self):
        return f"<Brand:{self.brand_name} Generic:{self.generic_name} Strength:{self.strength}>"


class Event(db.Model):
    """Refill events and reminders"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    start = db.Column(db.String(20), nullable=False)
    end = db.Column(db.String(20), nullable=True)
    all_day = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="events")

    def __repr__(self):
        return f"<Event:{self.id}; {self.title}>"


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
        return f"<Brand:{self.brand_name}, Generic:{self.generic_name} Strength:{self.strength}>"


if __name__ == "__main__":
    from server import app
    connect_to_db(app)