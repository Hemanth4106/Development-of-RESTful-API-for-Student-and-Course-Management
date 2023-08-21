from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///week7_database.sqlite3'

db = SQLAlchemy(app)
app.app_context().push()

class Student(db.Model):
  __tablename__ = 'student'
  student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  roll_number = db.Column(db.String, unique=True, nullable=False)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String)

class Course(db.Model):
  __tablename__ = 'course'
  course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  course_code = db.Column(db.String, unique=True, nullable=False)
  course_name = db.Column(db.String, nullable=False)
  course_description = db.Column(db.String)

class Enrollment(db.Model):
  __tablename__ = 'enrollments'
  enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  estudent_id = db.Column(db.Integer,db.ForeignKey("student.student_id",ondelete="CASCADE"),nullable=False)
  ecourse_id = db.Column(db.Integer,db.ForeignKey("course.course_id",ondelete="CASCADE"),nullable=False)
  student = db.relationship('Student', backref='enrollments')
  course = db.relationship('Course')

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll_number = request.form['roll']
        first_name = request.form['f_name']
        last_name = request.form['l_name']
        existing_student = Student.query.filter_by(roll_number=roll_number).first()
        if existing_student:
            return render_template('message.html')
        new_student = Student(roll_number=roll_number, first_name=first_name, last_name=last_name)
        db.session.add(new_student)
        db.session.commit()
        return redirect('/')
    return render_template('create_student.html')

@app.route('/course/create', methods=['GET', 'POST'])
def create_course_form():
    if request.method == 'POST':
        course_code = request.form['code']
        course_name = request.form['c_name']
        course_description = request.form['desc']
        existing_course = Course.query.filter_by(course_code=course_code).first()
        if existing_course:
            return render_template('course_already_exists.html')
        new_course = Course(course_code=course_code, course_name=course_name, course_description=course_description)
        db.session.add(new_course)
        db.session.commit()
        return redirect('/courses')
    else:
        return render_template('create_course.html')

    
@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get(student_id)
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        course_id = int(request.form['course'])
        Enrollment.query.filter_by(estudent_id=student_id).delete()
        enrollment = Enrollment(estudent_id=student_id, ecourse_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return redirect('/')
    else:
        courses = Course.query.all()
        return render_template('update_student.html', student=student, courses=courses)

@app.route('/course/<int:course_id>/update',methods=['GET', 'POST'])
def update_course_form(course_id):
    if request.method == 'POST':
        course = Course.query.get(course_id)
        course_name = request.form['c_name']
        course_description = request.form['desc']
        course.course_name = course_name
        course.course_description = course_description
        db.session.commit()
        return redirect('/courses')
    else:        
        course = Course.query.get(course_id)
        return render_template('update_course.html', course=course)


@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get(student_id)
    enrollments = Enrollment.query.filter_by(estudent_id=student_id).all()
    for enrollment in enrollments:
       db.session.delete(enrollment)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

@app.route('/course/<int:course_id>/delete')
def delete_course(course_id):
    course = Course.query.get(course_id)
    enrollments = Enrollment.query.filter_by(ecourse_id=course_id).all()
    for enrollment in enrollments:
       db.session.delete(enrollment)
    db.session.delete(course)
    db.session.commit()
    return redirect('/')

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get(student_id)
    enrollments = Enrollment.query.filter_by(estudent_id=student_id).all()
    courses = [enrollment.course for enrollment in enrollments]
    return render_template('student_details.html', student=student, courses=courses)

@app.route('/course/<int:course_id>')
def course_details(course_id):
    course = Course.query.get(course_id)
    enrolled_students = Enrollment.query.filter_by(ecourse_id=course_id).all()
    return render_template('course_details.html', course=course, enrolled_students=enrolled_students)

if __name__=="__main__":
   app.run()



