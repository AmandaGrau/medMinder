"""Models for prescription tracking app."""
from flask import Flask, session, render_template, url_for, request, flash, redirect
# Import SQLAlchemy constructor functionn
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance
db = SQLAlchemy()

# Connect flask app to database
def connect_to_db(flask_app, db_uri="postgresql:///prescriptions", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{'prescriptions'}"
    flask_app.config["SQLALCHEMY_ECHO"] = True
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initiate flask app
    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to db!")





class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    prescriptions = db.relationship("Prescription", back_populates="user")

    def __repr__(self):
        """Show user info."""

        return f"<user_id={self.user_id} fname={self.fname} email={self.email}"


# Table for user's prescribed medications
class Prescription(db.Model):
    """The user's prescribed medication."""

    __tablename__ = "prescriptions"

    prescription_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey("medications.medication_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    drug_name = db.Column(db.String)
    dosage_amount = db.Column(db.Integer)
    frequency_taken = db.Column(db.String)
    # refill_date = db.Column(db.DateTime)
    # Doctor class to be added in 2.0
    # doctor_id = db.Column(db.ForeignKey("doctor_id"))

    user = db.relationship("User", back_populates="prescriptions")
    medication = db.relationship("Medication", back_populates="prescriptions")

    def __repr__(self):
        """Show prescribed dosge, frequency taken, and refill due date."""

        return f"<Name: DOSE: {self.dosage_amount} TAKEN: {self.frequency_taken}.>"


# Table for all medications from API
class Medication(db.Model):
    """A medication."""

    __tablename__ = "medications"

    # drugs_API_id = db.Column(db.String)
    medication_id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String)
    generic_name = db.Column(db.String)

    prescriptions = db.relationship("Prescription", back_populates="medication")


    def __repr__(self):
        """Formal and generic medication names."""

        return f"<Brand brand_name={self.brand_name}, Generic generic_name={self.generic_name}>"


if __name__ == "__main__":
    from server import app
    # Function call connecting the app to database
    connect_to_db(app)