from dns.asyncresolver import resolve
from flask import  Flask, request
import bcrypt
import mysql.connector
import os, uuid
app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to the Seven SEAS API'

@app.route('/signup', methods = ['POST'])
def signup():
    res = request.form
    #TODO Change the dict key to the actual values used in the front end submit form
    user_email = res['user_email']
    user_password = res['password']
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), salt)


    conn = mysql.connector.connect(
        #TODO use env var in AWS for security
        host=os.getenv('db_uri'),
        user=os.getenv('db_username'),
        password=os.getenv('db_password'),
        database=os.getenv('db_name')
    )
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user (user_id, password, email)
        VALUES (%s, %s, %s)
    ''', (uuid.uuid4(), hashed_password, user_email))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)