import flask
from flask import Flask, render_template, request, url_for
import mysql.connector
from Classes import *

workshop_db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='database_workshop'
)

workshop_cursor = workshop_db.cursor()

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return f'main page'
    else:
        userName = request.form.get("username")
        userPassword = request.form.get("userpassword")

        # Check if user already exists in DB
        sql_q = "SELECT user_name FROM users WHERE user_name=%s and user_password=%s"
        param_q = (userName, userPassword)

        workshop_cursor.execute(sql_q, param_q)
        result = workshop_cursor.fetchone()

        if result is None:
            return "Error in login credentials"
        return f"{userName, userPassword} - You are now logged in"


@app.route("/login", methods=['GET'])
def login():
    return render_template("Login.html")

@app.route("/process_login", methods=['POST'])
def process_login():
    userName = request.form.get("username")
    userPassword = request.form.get("userpassword")

    if userName=="" or userPassword =="":
        return render_template("Login.html", user_error="All fields must have value")


    # Check if user already exists in DB
    sql_q = "SELECT user_name FROM users WHERE user_name=%s and user_password=%s"
    param_q = (userName, userPassword)

    workshop_cursor.execute(sql_q, param_q)
    result = workshop_cursor.fetchone()

    if result is None:
        return render_template("Login.html", user_error="Error in given credentials")


    return flask.redirect(url_for('target', name=userName, password=userPassword))


@app.route("/register", methods=['GET'])
def reg():
    return render_template("Register.html")


@app.route("/process-registration", methods=['POST'])
def handle2():
    userName = request.form.get("regUserName").strip()
    pw = request.form.get("regUserPw").strip()
    cnf_pw = request.form.get("cnfRegUserPw").strip()

    if userName == "" or pw == "" or cnf_pw == "":
        return render_template("Register.html", user_error="All fields must have value")
    if len(userName) > 45:
        return render_template("Register.html", user_error="User name is too long")

    # Check if user already exists in DB
    sql_q = "SELECT user_name FROM users WHERE user_name=%s"
    param_q = (userName, )
    workshop_cursor.execute(sql_q, param_q)

    if workshop_cursor.fetchone() is not None:
        return render_template("Register.html", user_error="User already exists")

    # Check matching password
    if cnf_pw == pw:
        # Add user to DB
        workshop_cursor.execute("INSERT INTO users(user_password, user_name) VALUES(%s, %s)", (pw, userName))
        workshop_db.commit()

        return flask.redirect(url_for('target', name=userName, password=pw))
    else:
        return render_template("Register.html", password_error="Passwords do not match")


@app.route("/target/<name>&<password>", methods=['GET', 'POST'])
def target(name, password):
    return f'{name} ***** {password} ***** {request.method}'
