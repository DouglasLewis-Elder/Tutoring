from flask import Flask, render_template
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


if __name__ == '__main__':
    app.run()