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

    def __repr__(self):
        """Show user info."""

        return f"<First:{self.fname} Last:{self.lname} Email:{self.email} Password:{self.password}>"


# Table for user's prescribed medications
class Prescription(db.Model):
    """The user's prescribed medication."""

    __tablename__ = "prescriptions"

    prescription_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.medication_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    brand_name = db.Column(db.String)
    generic_name = db.Column(db.String)
    unii = db.Column(db.String)
    dosage_form = db.Column(db.String)
    strength = db.Column(db.String)

    user = db.relationship("User", back_populates="prescriptions")
    medication = db.relationship("Medication", back_populates="prescriptions")

    def __repr__(self):
        """Show prescribed dosge, frequency taken, and refill due date."""

        return f"<Brand:{self.brand_name} Generic:{self.generic_name} Unii:{self.unii} Form:{self.dosage_form} Strength:{self.strength}>"


# Medications queried from Open FDA
class Medication(db.Model):
    """A medication."""

    __tablename__ = "medications"

    medication_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String)
    generic_name = db.Column(db.String)
    unii = db.Column(db.String)
    dosage_form = db.Column(db.String)
    strength = db.Column(db.String)

    prescriptions = db.relationship("Prescription", back_populates="medication")

    def __repr__(self):
        """Formal and generic medication names."""

        return f"<Brand:{self.brand_name}, Generic:{self.generic_name} Unii:{self.unii} Form:{self.dosage_form} Strength:{self.strength}>"


if __name__ == "__main__":
    from server import app
    # Function call connecting the app to database
    connect_to_db(app)