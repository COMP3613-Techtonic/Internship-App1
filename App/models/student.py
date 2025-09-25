from App.database import db
from App.models import User

class Student (User):
    __tablename__ = 'student'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    university = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False) 
    #one student can have more than one listing
    shortlist = db.relationship('Shortlist', backref='student', lazy=True)

    def __init__(self, username, password, university, major, year, telephone, email):
        super().__init__(username, password)
        self.university = university
        self.major = major
        self.year = year
        self.telephone = telephone
        self.email = email

    def __repr__(self):
        return f'<Employer ID: {self.id} - Username: {self.username} - University: {self.university}>'