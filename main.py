# x = 5
# if x == 5:
#     print("hello")

from flask import Flask, render_template, request



import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
cursor = conn.cursor()



python = Flask(__name__)

@python.route("/", methods=["GET"])

def home():
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
        sql = "SELECT * FROM cars"
        cursor.execute(sql)

    cars = cursor.fetchall()

    return render_template("index.html", cars=cars)





# @python.route("/dashboard", methods=["GET", "POST"])
# def dashboard():
#     msg = None

#     if request.method == "POST":
#         brand = request.form.get("brand")
#         model = request.form.get("model")
#         color = request.form.get("color")

#         sql = """
#             INSERT INTO cars (brand, model, color)
#             VALUES (%s, %s, %s)
#         """
#         cursor.execute(sql, (brand, model, color))
#         conn.commit()   # VERY IMPORTANT

#         msg = "Car added successfully!"


#     return render_template("dashboard.html", msg = msg)



@python.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    error = None
    success = None

    if request.method == "POST":
        brand = request.form.get("brand", "").strip()
        model = request.form.get("model", "").strip()
        color = request.form.get("color", "").strip()

        if not brand or not model or not color:
            error = "All fields are required."

        else:
            brand = brand.lower()
            model = model.lower()
            color = color.lower()

            check_sql = """
                SELECT id FROM cars
                WHERE brand = %s AND model = %s AND color = %s
            """
            cursor.execute(check_sql, (brand, model, color))
            existing_car = cursor.fetchone()

            if existing_car:
                error = "This car already exists in the database."
            else:
                insert_sql = """
                    INSERT INTO cars (brand, model, color)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(insert_sql, (brand, model, color))
                conn.commit()
                success = "Car added successfully!"

    return render_template("dashboard.html", error=error, success=success)





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
