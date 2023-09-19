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
    attendance_status = "Present"
    current_date = datetime.date.today()

    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="students"
    )

    cursor = conn.cursor()

    cursor.execute("SELECT sname FROM student WHERE srno = %s", (s_no,))
    result = cursor.fetchone()

    if result:
        student_name = result[0]
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


@app.route("/close_attendance", methods=["POST"])
def close_attendance():
    current_date = datetime.date.today()

    request_data = request.get_json()  # Get the JSON data from the request
    time_slot = int(request_data.get("time_slot"))
    print(time_slot)
    print(type(time_slot))

    conn = mysql.connector.connect(
        host="localhost", user="root", password="root", database="students"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT srno FROM student WHERE srno NOT IN (SELECT srno FROM attendance WHERE timeslot= %s)",
        (time_slot,),
    )
    absent_students = cursor.fetchall()
    print(time_slot)
    for student in absent_students:
        srno = student[0]
        cursor.execute(
            "INSERT INTO attendance (srno, timeslot, attendance_status, attendance_date) VALUES (%s, %s, %s, %s)",
            (srno, time_slot, "Absent", current_date),
        )
    conn.commit()
    conn.close()

    return "Attendance closed successfully!"


if __name__ == "__main__":
    app.run()
