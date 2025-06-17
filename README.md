
# medMinder

medMinder is a prescription tracking application that helps users manage their prescriptions and refill schedules. In using the application, users can search for medications, add, view, and delete prescriptions, as well as track refill dates through a calendar view.




## Tech Stack

**Front-end:** HTML, CSS, Bootstrap

**Back-end:** Python(Flask), Javascript

**Database:** PostgreSQL

**JavaScript Libraries:** FullCalendar



## Features

- User Authentication
- Prescription Management
- Calendar View
- Responsive Design


## Run Locally

To run the application locally on your machine, follow these steps:

```bash
  git clone https://github.com/AmandaGrau/capstone_project.git
```

Go to the project directory

```bash
  cd medMinder
```

Install dependencies

```bash
  pip install -r requirements.txt 
```

Set up PostgreSQL database
```
    Create a PostgreSQL database named prescriptions.
    Update the database URI in model.py to your local PostgreSQL database URI.
```

Start the server

```bash
  python3 server.py
```

Access the medMinder application

```bash
  The application can be accessed in your web browser at http://localhost:5000
```
That's it! You can now use medMinder locally on your machine. 
## Additional Installation Notes

This README assumes familiarity with setting up Python applications and PostgreSQL databases. If you encounter any difficulties during installation, please refer to the relevant documentation or seek assistance from a technical expert.