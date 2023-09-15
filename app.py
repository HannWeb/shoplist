from mysql.connector import (connection)
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """landing page when not logged in"""
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """landing page when logged in"""
    return render_template("dashboard.html")


@app.route("/login")
def login():
    """log in"""
    return render_template("login.html")


@app.route("/signup")
def signup():
    """sign up"""
    return render_template("signup.html")


@app.route("/new_product")
def new_product():
    """form to capture the new product"""
    return render_template("new_product.html")


@app.route("/list")
def products_list():
    """show list current or the one selected"""
    return render_template("list.html")


@app.route("/history")
def history():
    """show previous lists"""
    return render_template("history.html")