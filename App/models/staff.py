from App.database import db
from App.models import User

class Staff (User):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    university = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    #one staff member can be associated with more than one internship position listing
    shortlist = db.relationship('Shortlist', backref='staff', lazy=True) 

    def __init__(self, username, password, university, department, telephone, email):
        super().__init__(username, password)
        self.university = university
        self.department = department
        self.telephone = telephone
        self.email = email

    def __repr__(self):
        return f'<Staff ID: {self.id} - Username: {self.username} - University: {self.university}>'