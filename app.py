#Imports
from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error


#database
DATABASE = "tutor_db"
app = Flask(__name__)
def connect_to_database(db_file):
    try:
        con = sqlite3.connect(db_file)
        return con
    except Error:
        print("Failed to connect to DB")
    return

#ROUTES
@app.route('/') #Home route
def render_home():
    return render_template('home.html')

@app.route('/session_creation', methods=['POST','GET']) #Route for creating sessions
def render_sessions():

    if request.method == 'POST': #Gets data from the HTML file form
        tutor_id = request.form.get('tutor_id').title().strip()
        tutee_id = request.form.get('tutee_id').title().strip()
        time = request.form.get('time').title().strip()

        connection = connect_to_database(DATABASE)
        query_insert = "INSERT INTO sessions (tutor, tutee, time) VALUES (?,?,?)" #Puts into table
        cur = connection.cursor()
        cur.execute(query_insert, (tutor_id, tutee_id, time))
        connection.commit()
        connection.close()

    return render_template('sessions.html')

@app.route('/session_list')
def render_session_list():
    connection = connect_to_database(DATABASE)
    # Query like the others joinig the accounts table aswell to get the right names.
    query = ("""
        SELECT 
            session_id AS session_id,
            A1.first_name AS tutor_first_name, 
            A1.last_name AS tutor_last_name,
            A2.first_name AS tutee_first_name, 
            A2.last_name AS tutee_last_name,
            sessions.time AS session_time
        FROM 
            sessions
        JOIN accounts A1 ON sessions.tutor = A1.account_id
        JOIN accounts A2 ON sessions.tutee = A2.account_id
    """)

    cur = connection.cursor()
    cur.execute(query)
    session_list = cur.fetchall()
    connection.close()
    return render_template('session_list.html', session_list=session_list)


@app.route('/accounts') #Displays all the accounts
def render_accounts():
    connection = connect_to_database(DATABASE)
    query = "SELECT * FROM accounts"
    cur = connection.cursor()
    cur.execute(query)
    account_list = cur.fetchall()
    connection.close()
    return render_template('accounts.html', account_list=account_list)

@app.route('/signup', methods=['POST','GET'])
def render_signup():
    if request.method == 'POST': #getting the data that is from the form you fill out on the website
        first_n = request.form.get('user_first').title().strip()
        last_n = request.form.get('user_last').title().strip()
        email = request.form.get('user_email').lower().strip()
        tutor_type = request.form.get('tutor_check')
        pass1 = request.form.get('user_password')
        pass2 = request.form.get('user_password2')

        if pass1 != pass2: #checkes if boths passwrods are the same
            return redirect('\signup?error=passwords+do+not+match')

        if len(pass1) < 8: #password has to be over 8 characters
            return redirect('\signup?error=passwords+must+be+8+characters')

        connection = connect_to_database(DATABASE) # insertying more data in
        query_insert = "INSERT INTO accounts (first_name, last_name, type, email, pass) VALUES (?,?,?,?,?)"
        cur = connection.cursor()
        cur.execute(query_insert, (first_n, last_n, tutor_type, email, pass1))
        connection.commit()
        connection.close()

    return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def render_login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run()