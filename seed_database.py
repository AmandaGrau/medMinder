"""Script to auto seed the database."""

import os
# import json - will load with future imported data file

import crud
import model
import server

# Drop and re-create database
os.system("dropdb prescriptions")
os.system("createdb prescriptions")

# Connect to database through model.py, and call function to create db and tables
model.connect_to_db(server.app)
model.db.create.all()

# generate users and prescriptions to seed database
for n in range(15):
    email = f"user{n}@test.com"
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

model.db.session.commit()