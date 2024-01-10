"""Models for prescription tracking app."""

# Import SQLAlchemy constructor functionn
from flask_sqlalchemy import SQLAlchemy





# Create SQLAlchemy instance
db = SQLAlchemy()


 # Initiate flask app
# db.app = flask_app
# db.init_app(flask_app)

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


# Add db relationship


    def __repr__(self):
        """Show user info."""

        return f"<User_id={self.user_id} fname={self.fname} email={self.email}"



# class Prescription(db.Model):
#     """A medication prescribed to User."""

#     __tablename__ = "prescriptions"

#     medication_id = db.Column(db.Integer, db.ForeignKey("medication_id"))
#     user_id = db.Column(db.Integer, db.ForeignKey("user_id"))
#     doctor_id = db.Column(db.ForeignKey("doctor_id"))
#     dosage_amount = db.Column(db.Integer)
#     frequency_taken = db.Column(db.String)
#     refill_date = db.Column(db.Date)


# Add db relationship


    # def __repr__(self):
    #     """Show prescribed dosge, frequency taken, and refill due date."""

    #     return f"<DOSE {self.dosage_amount} TAKE {self.frequency_taken} REFILL {self.refill_date}.>"


# class Medication(db.Model):
#     """A medication."""

#     medication_id = db.Column(db.Integer, primary_key=True)
#     formal_name = db.Column(db.String)
#     generic_name = db.Column(db.String)


# Add db relationship


#     def __repr__(self):
#         """Formal and generic medication names."""

#         return f"<Brand formal_name={self.formal_name}, generic generic_name={self.generic_name}>"




# Connect flask app to database
def connect_to_db(flask_app, db_uri="postgresql:///prescriptions", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

   



if __name__ == "__main__":

    # Should run properly once server.py content is created
    # from server import app

    # Connect to database and confirm successful connection
    connect_to_db(app)
    print("Connected to db!")