from App.database import db
from App.models import User

class Employer(User):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    # an employer can have more than one internship positions available
    positions = db.relationship('Position', backref='employer', lazy=True)

    def __init__(self, username, password, company, department, telephone, email):
        super().__init__(username, password)
        self.company = company
        self.department = department
        self.telephone = telephone
        self.email = email

    def __repr__(self):
        return f'<Employer ID: {self.id} - Username: {self.username} - Company: {self.company}>'