"""Generate fifteen fake users to seed the database."""

import os
import crud
import model
import server

# Drop and re-create database
os.system("dropdb prescriptions")
os.system("createdb prescriptions")

# Connect to database and create tables
model.connect_to_db(server.app)
model.db.create_all()

# Generate fake users to seed database
for n in range(15):
    fname = 'testFname'
    lname = 'testLname'
    email = f"user{n}@test.com"
    # Will be hashed in add_new_user
    password = "test"

    # Create user with hashed password
    user = crud.add_new_user(fname, lname, email, password, totp_secret=None)

    model.db.session.add(user)
    
# Commit all users at once
model.db.session.commit()