from flask import Flask, render_template, request
import mysql.connector
import datetime

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/process_data", methods=["POST"])
def process_data():
    s_no = request.form.get("student_roll_no")
    time_slot = request.form.get("time_slot")
    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="students"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT sname FROM student WHERE srno = %s", (s_no,))
    result = cursor.fetchone()

    if result:
        student_name = result[0]
        attendance_status = "Present"
        current_date = datetime.date.today()

        cursor.execute(
            "INSERT INTO attendance (srno, timeslot, attendance_status, attendance_date) VALUES (%s, %s, %s, %s)",
            (s_no, time_slot, attendance_status, current_date),
        )
        conn.commit()
    else:
        student_name = "Student not found"

    conn.close()

    return render_template(
        "index.html",
        student_roll_no=s_no,
        student_name=student_name,
        time_slot=time_slot,
    )


if __name__ == "__main__":
    app.run()
