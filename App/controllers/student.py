from App.models.student import Student
from App.database import db
from App.controllers.user import *
from App.controllers.shortlist import *

def create_student(username, password, university, major, year, telephone, email):
    newStudent = Student(username=username, password=password, university=university, major=major, year=year, telephone=telephone, email=email)
    db.session.add(newStudent)
    db.session.commit()
    return newStudent

def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()

def get_student(student_id):
    return Student.query.get(student_id)

def get_all_students():
    return Student.query.all()

def update_student(student_id, username, university, major, year, telephone, email):
    student = get_student(student_id)
    if student:
        update_user(student_id, username)
        student.university=university
        student.major=major
        student.year=year
        student.telephone=telephone
        student.email=email
        db.session.add(student)
        db.session.commit()
        return student
    return "Student not found"

def view_student_listing(student_id):
    student = get_student(student_id)
    if student:
        list = get_student_shortlist(student_id)
        if list:
            return list
        return "No listings available"
    return "Student not found"

def view_response(student_id, status):
    student = get_student(student_id)
    if student:
        list = Shortlist.query.filter_by(student_id=student_id, status=status).all()
        if list:
            return list
        return "No responses available"
    return "Student not found"