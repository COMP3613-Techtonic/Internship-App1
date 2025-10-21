from App.database import db

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    # an employer can have more than one internship positions available
    shortlist = db.relationship('Shortlist', backref='position', lazy=True)

    def __init__(self, title, description, requirements, location, employer_id):
        self.title = title
        self.description = description
        self.requirements = requirements
        self.location = location
        self.employer_id = employer_id
        
    def __repr__(self):
        return f'<Position ID: {self.id} - title: {self.title} - Description: {self.description} - Requirements: {self.requirements} - Location: {self.location} - Employer ID: {self.employer_id}>'