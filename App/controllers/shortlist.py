from App.models.shortlist import Shortlist
from App.models.position import Position
from App.database import db

def create_listing(internship_id, student_id, staff_id):
    newListing = Shortlist(internship_id=internship_id, student_id=student_id, staff_id=staff_id, status="Pending")
    db.session.add(newListing)
    db.session.commit()
    return newListing

def get_listing(listing_id):
    return Shortlist.query.get(listing_id)

def get_all_listings():
    return Shortlist.query.all()

def get_employer_shortlist(employer_id):
    return Shortlist.query.join(Position).filter_by(employer_id=employer_id).all()

def get_student_shortlist(student_id):
    return Shortlist.query.filter_by(student_id=student_id).all()

def get_staff_shortlist(staff_id):
    return Shortlist.query.filter_by(staff_id=staff_id).all()

def update_listing(listing_id, internship_id, student_id, staff_id):
    listing = get_listing(listing_id)
    if listing:
        listing.internship_id = internship_id
        listing.student_id = student_id
        listing.staff_id = staff_id
        db.session.add(listing)
        db.session.commit()
        return listing
    return "Listing not found"