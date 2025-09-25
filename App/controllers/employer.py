from App.models.employer import Employer
from App.database import db
from App.controllers.user import *
from App.controllers.position import *
from App.controllers.shortlist import *

def create_employer(username, password, company, department, telephone, email):
    newEmployer = Employer(username=username, password=password, company=company, department=department, telephone=telephone, email=email)
    db.session.add(newEmployer)
    db.session.commit()
    return newEmployer

def get_employer_by_username(username):
    return Employer.query.filter_by(username=username).first()

def get_employer(employer_id):
    return Employer.query.get(employer_id)

def get_all_employers():
    return Employer.query.all()

def update_employer(employer_id, username, company, department, telephone, email):
    employer = get_employer(employer_id)
    if employer:
        update_user(employer_id, username)
        employer.company=company
        employer.department = department
        employer.telephone=telephone
        employer.email=email
        db.session.add(employer)
        db.session.commit()
        return employer
    return "Employer not found"

#viewing all internship positions created
def view_positions(employer_id):
    employer = get_employer(employer_id)
    if employer:
        if not employer.positions:
            return "No positions found for this employer"
        return employer.positions
    return "Employer not found"
    
def view_shortlist(employer_id):
    employer = get_employer(employer_id)
    if employer:
        list = get_employer_shortlist(employer_id)
        if list:
            return list
        return "No shortlist available"
    return "Employer not found"

def respond(employer_id, listing_id, response):
    employer = get_employer(employer_id)
    if employer:
        listing = get_listing(listing_id)
        if listing and listing.position.employer_id==int(employer_id):
            listing.status = response
            db.session.commit()
            return listing
        return "Listing not found for employer"
    return "Employer not found"