from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, db, read_db_response, validate_field

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure database
db = db()


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


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """landing page when logged in"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("name"):
            return apology("A list name should be provided", 400)
        # Ensure user us logged in
        if not session["user_id"]:
            return redirect("/login")

        # Write list on the database
        cursor = db.cursor()
        add_lists = "INSERT INTO lists (name, user_id) VALUES (%s, %s)"
        data_lists = (request.form.get("name"), session["user_id"])
        cursor.execute(add_lists, data_lists)
        db.commit()
        cursor.close()
        return redirect("/dashboard")
    else:
        cursor = db.cursor()
        query_user = "SELECT id, name FROM lists WHERE user_id = %s"
        cursor.execute(query_user, [session["user_id"]])
        data = read_db_response(cursor)
        return render_template("dashboard.html", lists=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """log in"""
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        # ensure username does exist in the database.
        cursor = db.cursor()
        query_user = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query_user, [request.form.get("username")])
        data = read_db_response(cursor)
        if len(data) != 1 or not check_password_hash(data[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = data[0][0]
        session["first_name"] = data[0][3]
        session["last_name"] = data[0][3]
        return redirect("/dashboard")

    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """sign up"""
    if request.method == "POST":
        # Ensure Name was submitted
        if not request.form.get("first_name"):
            return apology("Must provide first name", 400)
        if not request.form.get("last_name"):
            return apology("Must provide last name", 400)
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password was submitted
        if not request.form.get("confirmation"):
            return apology("Must provide a password confirmation", 400)
        # store variables for management
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # ensure username does exist in the database.
        cursor = db.cursor()
        query_user = "SELECT username FROM users WHERE username = %s"
        cursor.execute(query_user, [username])
        data = read_db_response(cursor)
        if len(data) >= 1:
            return apology("Username not available", 400)
        # write data on db
        cursor = db.cursor()
        add_user = "INSERT INTO users (first_name, last_name, username, hash) VALUES (%s, %s, %s, %s )"
        data_user = (first_name, last_name, username, generate_password_hash(password))
        cursor.execute(add_user, data_user)
        user_id = cursor.lastrowid
        db.commit()
        cursor.close()
        session["user_id"] = user_id
        session["first_name"] = first_name
        session["last_name"] = last_name
        return redirect("/dashboard")
    else:
        return render_template("signup.html")


@app.route("/new_product", methods=["GET", "POST"])
@login_required
def new_product():
    if request.method == "POST":
        # list of fields
        fields = ["barcode", "name", "quantity", "price", "store"]

        # Ensure all fields were submitted
        for field in fields:
            if not request.form.get(field):
                print("field ", field, ": ", request.form.get(field))
                return apology(f"Must provide {field}", 400)

        # Assign variable to form data
        barcode = request.form.get("barcode")
        name = request.form.get("name")
        category = request.form.get("category")
        package = 0 if not request.form.get("package") else request.form.get("package")
        pkg_units = 0 if not request.form.get("pkg_units") else request.form.get("pkg_units")
        in_cart = 1  # need to figure it out

        # Ensure product not exist in the database
        cursor = db.cursor()
        query_product = "SELECT id FROM products WHERE barcode = %s AND user_id = %s"
        data_product = (barcode, session["user_id"])
        cursor.execute(query_product, data_product)
        data = read_db_response(cursor)

        # Open data base session
        cursor = db.cursor()

        # if it is a new product add product
        if len(data) == 0:
            # Add product
            add_product = "insert into products (barcode, name, category, user_id) values (%s, %s, %s, %s)"
            data_product = (barcode, name, category, session["user_id"])
            cursor.execute(add_product, data_product)
            # save product id:
            session["product_id"] = cursor.lastrowid
        else:
            update_product = "UPDATE products SET name=%s, category=%s WHERE barcode=%s AND user_id=%s"
            product_data = (name, category, barcode, session["user_id"])
            cursor.execute(update_product, product_data)
            # save product id:
            session["product_id"] = data[0][0]

        # add price
        add_price = "insert into prices " \
                    "(product_id, store_id, package," \
                    "package_units, user_id, list_id, in_cart, price, quantity) " \
                    "values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # store product id value
        data_price = (session.get("product_id"), 1, package, pkg_units, session["user_id"],
                      session["list_id"], in_cart, request.form.get("price"), request.form.get("quantity"))
        cursor.execute(add_price, data_price)
        db.commit()
        cursor.close()
        # TODO: how not store the same price multiple times (updating the product of the same day?)
        return redirect(url_for("products_list", list_id=session.get("list_id")))
    else:
        return render_template("new_product.html")


@app.route("/list")
def products_list():
    # TODO: display products in a list, if more than instance of the same product. show the latest
    print(request.args)
    if "list_id" not in request.args:
        return apology("Invalid List", 400)
    session["list_id"] = request.args.get("list_id")
    return render_template("list.html")


@app.route("/history")
def history():
    """show previous lists"""
    return render_template("history.html")
