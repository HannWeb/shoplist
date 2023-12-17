import mysql.connector
from mysql.connector import errorcode
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# Configure database
def db():
    try:
        config = {"user": "hannqzwz_superuser", "password": "7a_GG@5z$azU",
                  "host": "127.0.0.1",
                  "port": "3306",
                  "database": "hannqzwz_shop"}
        cnx = mysql.connector.connect(**config)
        print(f"connected on port {config['port']}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx


def read_db_response(cursor):
    data = []
    for value in cursor:
        data.append(value)
    cursor.close()
    return data


def validate_field(source, field_name):
    if source.method == "POST":
        if not source.form.get(field_name):
            print("source", source.form.get(field_name))
            return apology("Must provide barcode", 400)

    if source.method == "GET":
        print(source.args)


def currency(value):
    """Format value as USD."""
    return f"${value:,.2f}"