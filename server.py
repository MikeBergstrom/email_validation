from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app,'emails')
app.secret_key='secrety'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
@app.route('/')
def index():
    query = "SELECT email, DATE_FORMAT(created_at, '%c/%e/%Y %I:%i') as created FROM emails"
    emails = mysql.query_db(query)
    return render_template('index.html', all_emails=emails)
@app.route('/input', methods=['POST'])
def create():
    # add an email to the database!
    if not EMAIL_REGEX.match(request.form['email']):
        return render_template('fail.html')
    else:
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
        data = {
            'email': request.form['email'],
        }
        mysql.query_db(query, data)
        session['email'] = request.form['email']
        return redirect('/success')

@app.route('/success')
def success():
    query = "SELECT email, DATE_FORMAT(created_at, '%c/%e/%Y %I:%i%p') as created FROM emails"
    emails = mysql.query_db(query)
    return render_template('success.html', all_emails=emails)

@app.route('/delete', methods=['POST'])
def delete():
    session['email'] = request.form['email']
    query = "DELETE FROM emails WHERE email = :email"
    data = {'email': request.form['email']}
    mysql.query_db(query, data)
    query = "SELECT email, DATE_FORMAT(created_at, '%c/%e/%Y %I:%i%p') as created FROM emails"
    emails = mysql.query_db(query)
    return render_template('delete.html', all_emails=emails)

app.run(debug=True)