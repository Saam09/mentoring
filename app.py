from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/process_data', methods=['POST'])
def process_data():
    student_roll_no = request.form.get('student_roll_no')
    student_name = 'abcdes'
    
    return render_template('index.html', student_roll_no=student_roll_no,student_name = student_name)

if __name__ == '__main__':
    app.run()
