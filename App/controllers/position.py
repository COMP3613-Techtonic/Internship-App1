from App.models.position import Position
from App.database import db

def create_position(title, description, requirements, location, employer_id):
    newPosition = Position(title=title, description=description, requirements=requirements, location=location, employer_id=employer_id)
    db.session.add(newPosition)
    db.session.commit()
    return newPosition

def get_position_by_title(title):
    return Position.query.filter_by(title=title).first()

def get_position(position_id):
    return Position.query.get(position_id)

def get_all_positions():
    return Position.query.all()

def update_position(position_id, description, requirements, location, employer_id):
    position = get_position(position_id)
    '''if not position:
        return "Internship position not found"
    else:'''
    position.description = description
    position.requirements = requirements
    position.location = location
    position.employer_id = employer_id
    db.session.add(position)
    db.session.commit()
    return position