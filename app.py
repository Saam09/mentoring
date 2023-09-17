from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/process_data", methods=["POST"])
def process_data():
    s_no = request.form.get("student_roll_no")

    # Connect to your SQLite database (change the database path accordingly)
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="students"
    )

    cursor = conn.cursor()

    # Execute a SQL query to retrieve the sname based on the student_roll_no
    cursor.execute("SELECT sname FROM student WHERE srno = %s", (s_no,))
    result = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Check if a result was found
    if result:
        student_name = result[0]  # Extract the student name from the result
    else:
        student_name = "Student not found"

    return render_template(
        "index.html", student_roll_no=s_no, student_name=student_name
    )


if __name__ == "__main__":
    app.run()
