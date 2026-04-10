from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, url_for, session
from functools import wraps
from datetime import timedelta

import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
cursor = conn.cursor()



python = Flask(__name__)


# For session data → encrypted using secret_key → stored in browser
python.secret_key = "my_super_secret_key_123"


# Homne Page
@python.route("/", methods=["GET"])
def home():
    # if "user_key" not in session:
    #     print("hello")


    search_car = request.args.get("search")

    if search_car:
        sql = """
            SELECT * FROM cars
            WHERE model LIKE %s
               OR brand LIKE %s
               OR color LIKE %s
        """
        value = f"%{search_car}%"

        cursor.execute(sql, (value, value, value))

    else:
        sql ="""
           SELECT 
           cars.id,
           cars.brand,
           cars.model,
           cars.color,
           carsmeta.car_number,
           carsmeta.registration_no
           FROM cars
           LEFT JOIN carsmeta
           ON cars.id = carsmeta.id 
        """
        cursor.execute(sql)

    cars = cursor.fetchall()

    return render_template("index.html", cars=cars)





# Dashboard Page
@python.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "user_ID" not in session:
        return redirect(url_for("login"))
        
    
    else :
        sql = "SELECT * FROM cars"
        cursor.execute(sql)
        cars = cursor.fetchall()

        error = None
        success = None

        if request.method == "POST":
            brand = request.form.get("brand", "").strip()
            model = request.form.get("model", "").strip()
            color = request.form.get("color", "").strip()
            car_number = request.form.get("car_number", "").strip()
            registration = request.form.get("registration_no", "").strip()

            if not brand or not model or not color or not car_number or not registration:
                error = "All fields are required."

            else:
                brand = brand.lower()
                model = model.lower()
                color = color.lower()
                car_number = car_number.lower()
                registration = registration.lower()

                check_sql = """
                    SELECT cars.id
                    FROM cars
                    LEFT JOIN carsmeta ON cars.id = carsmeta.id
                    WHERE brand = %s
                    AND model = %s
                    AND color = %s
                    AND car_number = %s
                    AND registration_no = %s
                """
                cursor.execute(check_sql, (brand, model, color, car_number, registration))
                existing_car = cursor.fetchone()

                if existing_car:
                    error = "This car already exists in the database."
                else:
                    # Insert into cars table
                    insert_car_sql = """
                        INSERT INTO cars (brand, model, color)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_car_sql, (brand, model, color))
                    conn.commit()

                    car_id = cursor.lastrowid  # Get inserted car ID

                    # Insert into carsmeta table
                    insert_meta_sql = """
                        INSERT INTO carsmeta (id, car_number, registration_no)
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_meta_sql, (car_id, car_number, registration))
                    conn.commit()

                    return redirect(url_for("dashboard"))
                    
        new_cars_added_sql = """
            SELECT * FROM cars
        """
        cursor.execute(new_cars_added_sql)
        cars = cursor.fetchall()
        # cursor.close()
            

    return render_template("dashboard.html", error=error, success=success, cars = cars)







# Login Page
@python.route("/login", methods=["GET", "POST"])
def login():

    if "user_ID" in session:
        return redirect(url_for("dashboard"))

    login_success = None
    error = None

    if request.method == "POST":

        user = request.form.get("user", "").strip()
        password = request.form.get("password", "").strip()

      
        check_sql = """
            SELECT * FROM users
            WHERE userID = %s OR email = %s
        """

        cursor.execute(check_sql, (user, user))
        known_account = cursor.fetchone()

        if known_account:

            stored_user = known_account[2]
            stored_password = known_account[3]  # adjust index if needed

            if check_password_hash(stored_password, password):

                session["user_ID"] = stored_user
                # session.permanent = True

                if request.form.get("remember_me"):
                    session.permanent = True
                    python.permanent_session_lifetime = timedelta(seconds = 5)
                else:
                    session.permanent = True


                login_success = "Login Successfully."
                return redirect(url_for("dashboard"))

            else:
                error = "Invalid Password!!Try Again"       

        else:
            error = "User not found. Create an account!"

    return render_template("login.html",login_success=login_success,error=error)




#Log Out Page
@python.route("/logout", methods = ["GET"])
def logout():
    session.clear()

    return redirect(url_for("login"))



# Register Page
@python.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None

    if request.method == "POST":
        fullname = request.form.get("fullname", "").strip()
        userID = request.form.get("user", "").strip()
        password = request.form.get("password", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()

        if not all([fullname, userID, password, phone, email]):
            error = "All fields are required."

        else:
            check_sql = """
                SELECT id FROM users
                WHERE email = %s OR userID = %s OR phoneNumber = %s
            """

            cursor.execute(check_sql, (email, userID, phone))
            existing_account = cursor.fetchone()

            if existing_account:
                error = "Already account exist!!"

            else:
                hashed_password = generate_password_hash(password)

                insert_sql = """
                    INSERT INTO users 
                    (fullname, userID, password, phoneNumber, email)
                    VALUES (%s, %s, %s, %s, %s)
                """

                cursor.execute(insert_sql, (fullname,userID,hashed_password, phone,email))

                conn.commit()
                success = "Registration successful!"

    return render_template("register.html", error=error, success=success)   






if __name__ == "__main__":
    python.run(debug=True)











# sql = """
# INSERT INTO cars (model, brand, color)
# VALUES (%s, %s, %s)
# """
# # values = ("Brezza", "Maruti", "black")

# # cursor.execute(sql, values)
# conn.commit()
# conn.close()
# print("data inserted in the table.")
