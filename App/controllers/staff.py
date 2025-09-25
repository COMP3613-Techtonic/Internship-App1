from App.models.staff import Staff
from App.database import db
from App.controllers.user import *
from App.controllers.student import *
from App.controllers.position import *

def create_staff(username, password, university, department, telephone, email):
    newStaff = Staff(username=username, password=password, university=university, department=department, telephone=telephone, email=email)
    db.session.add(newStaff)
    db.session.commit()
    return newStaff

def get_staff_by_username(username):
    return Staff.query.filter_by(username=username).first()

def get_staff(staff_id):
    return Staff.query.get(staff_id)

def get_all_staff():
    return Staff.query.all()

def update_staff(staff_id, username, university, department, telephone, email):
    staff = get_staff(staff_id)
    if staff:
        update_user(staff_id, username)
        staff.university=university
        staff.department=department
        staff.telephone=telephone
        staff.email=email
        db.session.add(staff)
        db.session.commit()
        return staff
    return "Staff member not found"

def add_student(staff_id, student_id, position_id):
    staff = get_staff(staff_id)
    if staff:
        position = get_position(position_id)
        if position:
            student = get_student(student_id)
            if student:
                #status="Pending"
                listing = create_listing(position.id, student.id, staff_id)
                return listing
            return "Student does not exist"
        return "Position does not exist"
    return "Staff member does not exist"

def view_staff_listing(staff_id):
    staff = get_staff(staff_id)
    if staff:
        list = get_staff_shortlist(staff_id)
        if list:
            return list
        return "No listings available"
    else:
        return "Staff member not found"
