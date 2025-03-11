from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error


DATABASE = "tutor_db"
app = Flask(__name__)

def connect_to_database(db_file):
    try:
        con = sqlite3.connect(db_file)
        return con
    except Error:
        print("Failed to connect to DB")
    return

@app.route('/')
def render_home():
    return render_template('home.html')

@app.route('/sessions')
def render_sessions():
    return render_template('sessions.html')


@app.route('/accounts')
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
    if request.method == 'POST':
        first_n = request.form.get('user_first').title().strip()
        last_n = request.form.get('user_last').title().strip()
        email = request.form.get('user_email').lower().strip()
        tutor_type = request.form.get('tutor_check')
        print(tutor_type)
        pass1 = request.form.get('user_password')
        pass2 = request.form.get('user_password2')

        if pass1 != pass2:
            return redirect('\signup?error=passwords+do+not+match')

        if len(pass1) < 8:
            return redirect('\signup?error=passwords+must+be+8+characters')

        connection = connect_to_database(DATABASE)
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