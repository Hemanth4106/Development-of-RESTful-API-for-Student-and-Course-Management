from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource,reqparse,abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///api_database.sqlite3"

db = SQLAlchemy(app)
api=Api(app)

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
  course_name = db.Column(db.String, nullable=False)
  course_code = db.Column(db.String, unique=True, nullable=False)
  course_description = db.Column(db.String)

class Enrollment(db.Model):
   __tablename__ = 'enrollment'
   enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   student_id = db.Column(db.Integer,db.ForeignKey("student.student_id"),nullable=False)
   course_id = db.Column(db.Integer,db.ForeignKey("course.course_id"),nullable=False)

course_parser = reqparse.RequestParser()
course_parser.add_argument('course_name', type=str, required=True, help='Course Name is required.')
course_parser.add_argument('course_code', type=str, required=True, help='Course Code is required.')
course_parser.add_argument('course_description', type=str)

student_parser = reqparse.RequestParser()
student_parser.add_argument('roll_number', type=str, required=True, help='Roll Number is required.')
student_parser.add_argument('first_name', type=str, required=True, help='First Name is required.')
student_parser.add_argument('last_name', type=str)

enrollment_parser = reqparse.RequestParser()
enrollment_parser.add_argument('course_id', type=int, required=True, help='Course ID is required.')    
 
class CourseApi(Resource):
    def get(self,course_id):
        course=Course.query.filter_by(course_id=course_id).first()
        if course:
            return {
                "course_id": course.course_id,
                "course_name": course.course_name,
                "course_code": course.course_code,
                "course_description": course.course_description
            },200
        else:
            return{
                "message": "Course not found"
            },404
 
    def put(self, course_id):
        args=course_parser.parse_args()
        course=Course.query.get(course_id)
        if course:
            if args["course_name"] is None:
                return{
                    "error_code": "COURSE001",
                    "error_message": "Course Name is required"
                },400
            elif args["course_code"] is None:
                return{
                    "error_code": "COURSE002",
                    "error_message": "Course Code is required"
                },400   
        else:
            return {
                "message": "Course not found"
            },404
        course.course_name=args["course_name"]
        course.course_code=args["course_code"]
        course.course_description=args["course_description"]
        db.session.commit()
        return {
            "course_id": course.course_id,
            "course_name": course.course_name,
            "course_code": course.course_code,
            "course_description": course.course_description
        },200

    def delete(self, course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()
            return{
                "message": "Successfully Deleted"
            },200
        else:
            return {
                "message": "Course not found"
            },404
        
    def post(self):
        args = course_parser.parse_args()
        course_name = args["course_name"]
        course_code = args["course_code"]
        course_description=args["course_description"]
        c=Course.query.filter_by(course_code=course_code).first()
        if course_name is None:
            return{
                "error_code": "COURSE001",
                "error_message": "Course Name is required"
            },400

        elif course_code is None:
            return{
                "error_code": "COURSE002",
                "error_message": "Course Code is required"
            },400
        elif c:
            return{
                "message": "course_code already exist"
            },409

        new_course = Course(course_name=course_name,course_code=course_code,course_description=course_description)
        db.session.add(new_course)
        db.session.commit()
        return {
            "course_id": new_course.course_id,
            "course_name": new_course.course_name,
            "course_code": new_course.course_code,
            "course_description": new_course.course_description

        },201
    
class StudentApi(Resource):
   def get(self,student_id):
      student=Student.query.filter_by(student_id=student_id).first()
      if student:
          return {
              "student_id": student.student_id,
              "first_name": student.first_name,
              "last_name": student.last_name,
              "roll_number": student.roll_number
          },200
      else:
          return{
              "message": "Student not found"
          },404
      
   def put(self,student_id):
        args=student_parser.parse_args()
        student=Student.query.get(student_id)
        if student:
            if args["roll_number"] is None:
                return{
                    "error_code": "STUDENT001",
                    "error_message": "Roll Number required"
                },400
            elif args["first_name"] is None:
                return{
                    "error_code": "STUDENT002",
                    "error_message": "First Name is required"
                },400   
        else:
            return {
                "message": "Student not found"
            },404
        student.first_name=args["first_name"]
        student.last_name=args["last_name"]
        student.roll_number=args["roll_number"]
        db.session.commit()
        return {
            "student_id": student.student_id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "roll_number": student.roll_number
        },200
       
   def delete(self, student_id):
        student = Student.query.get(student_id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return{
                "message": "Successfully Deleted"
            },200
        else:
            return {
                "message": "Student not found"
            },404
      
   def post(self):
       args = student_parser.parse_args()
       roll_number = args["roll_number"]
       first_name = args["first_name"]
       last_name=args["last_name"]
       c=Student.query.filter_by(roll_number=roll_number).first()
       if roll_number is None:
            return{
                "error_code": "STUDENT001",
                "error_message": "Roll Number is required"
            },400

       elif first_name is None:
            return{
                "error_code": "STUDENT002",
                "error_message": "First Name is required"
            },400
       
       elif c:
            return{
                "message": "Student already exist"
            },409

       new_student = Student(roll_number=roll_number,first_name=first_name,last_name=last_name)
       db.session.add(new_student)
       db.session.commit()
       return {
            "student_id": new_student.student_id,
            "first_name": new_student.first_name,
            "last_name": new_student.last_name,
            "roll_number": new_student.roll_number
        },201
    
class EnrollmentApi(Resource):
    def get(self,student_id):
        if student_id:
            student=Student.query.filter_by(student_id=student_id).first()
            if student is None:
                return {
                        "error_code":"ENROLLMENT002",
                        "error_message":"Student does not exist"
                    },400
            else:
                enrollments = Enrollment.query.filter_by(student_id=student_id).all()
                if enrollments:
                    allenroll=[]
                    for enroll in enrollments:
                        thisenroll={}
                        thisenroll['enrollment_id']=enroll.enrollment_id
                        thisenroll["student_id"]=enroll.student_id
                        thisenroll["course_id"]=enroll.course_id
                        allenroll.append(thisenroll)
                    return allenroll,200
                else:
                    return{
                        "message":"Student is not enrolled in any course"
                    },404      
        
    def delete(self,student_id,course_id):
        course = Course.query.filter_by(course_id=course_id).first()
        student = Student.query.filter_by(student_id=student_id).first()
        enroll=Enrollment.query.filter_by(student_id=student_id).first()
        if course is None:
            return{
                "error_code": "ENROLLMENT001",
                "error_message": "Course does not exist"
            },400
        elif student is None:
            return{
                "error_code": "ENROLLMENT002",
                "error_message": "Student does not exist"
            },400
        elif enroll is None:
            return{
                "message": "Enrollment for the student not found"
            },404
        to_delete=Enrollment.query.filter_by(student_id=student_id,course_id=course_id).first()
        db.session.delete(to_delete)
        db.session.commit()
        return{
            "message": "Successfully deleted"
        },200

    def post(self,student_id):
        args=enrollment_parser.parse_args()
        course_id=args["course_id"]
        course=Course.query.filter_by(course_id=course_id).first()
        student=Student.query.filter_by(student_id=student_id).first()
        if course is None:
            return{
                "error_code": "ENROLLMENT001",
                "error_message": "Course does not exist"
            },400
        elif student is None:
            return{
                "message": "Student not found"
            },404
        new_enroll=Enrollment(course_id=course_id,student_id=student_id)
        db.session.add(new_enroll)
        db.session.commit()
        return{
            "enrollment_id": new_enroll.enrollment_id,
            "student_id": new_enroll.student_id,
            "course_id": new_enroll.course_id
        },201

api.add_resource(CourseApi, "/api/course", "/api/course/<int:course_id>")
api.add_resource(StudentApi, "/api/student", "/api/student/<int:student_id>")
api.add_resource(EnrollmentApi, "/api/student/<int:student_id>/course", "/api/student/<int:student_id>/course/<int:course_id>")

if __name__=="__main__":
   app.run()