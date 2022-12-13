# Knowledge Based Autocomplete Name Search

Homework done for the RTU - Development Methods of Applied Intelligent Software Systems class.

To launch the application, download the required libraries (see `requirements.txt`) and launch the script `python3 index.py` from the base directory of the project.
A web server will launch on port 5000 (http://localhost:5000).

You have a simple page to test the autocomplete on the root page of the webserver (http://localhost:5000)

The api have 2 endpoints:
  - `http://localhost:5000/find` is a GET endpoint that take the 'find' parameter with the string the user entered
  - `http://localhost:5000/submit` is a POST endpoint that take in the body a JSON with two attributes:
    - `chosen` who contains the submitted value
    - `suggestions` who contains all the values that where proposed to the user (including the chosen value)

The database used is a Sqlite database, if the database does not exists, it will create it at start with a set of randomly default name (found in `database/initial_values.sql`).