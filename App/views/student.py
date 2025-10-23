"""
Student-related endpoints.

Routes (blueprint prefix='/student'):
- POST   /student/                    -> create student
- GET    /student/                    -> list students
- GET    /student/<id>/shortlist      -> view shortlist for a student (auth)
- GET    /student/<id>/responses      -> view responses filtered by status (auth)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    create_student,
    get_all_students,
    view_student_listing,
    view_response
)

student_view = Blueprint('student', __name__, url_prefix='/student')


@student_view.route('/', methods=['POST'])
def create_student_route():
    """
    Create student account.
    Body JSON: { username, password, university, major, year, telephone, email }
    """
    data = request.get_json() or {}
    required = ['username', 'password', 'university', 'major', 'year', 'telephone', 'email']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    s = create_student(
        data['username'],
        data['password'],
        data['university'],
        data['major'],
        data['year'],
        data['telephone'],
        data['email']
    )
    return jsonify({"message": "Student created", "id": s.id}), 201


@student_view.route('/', methods=['GET'])
def list_students_route():
    students = get_all_students()
    result = []
    for s in students:
        result.append({
            "id": s.id,
            "username": s.username,
            "university": getattr(s, "university", None)
        })
    return jsonify(result), 200


@student_view.route('/<int:student_id>/shortlist', methods=['GET'])
@jwt_required()
def student_shortlist_route(student_id):
    """
    Student views their shortlist entries.
    """
    listings = view_student_listing(student_id)
    if isinstance(listings, str):
        return jsonify({"message": listings}), 404
    result = []
    for l in listings:
        result.append({
            "id": l.id,
            "internship_id": l.internship_id,
            "status": l.status,
            "staff_id": l.staff_id
        })
    return jsonify(result), 200


@student_view.route('/<int:student_id>/responses', methods=['GET'])
@jwt_required()
def student_responses_route(student_id):
    """
    View responses filtered by status. Query param: ?status=Accepted|Rejected|Pending
    """
    status = request.args.get('status', None)
    if not status:
        return jsonify({"error": "Provide status query param e.g. ?status=Accepted"}), 400

    listings = view_response(student_id, status)
    if isinstance(listings, str):
        return jsonify({"message": listings}), 404

    result = []
    for l in listings:
        result.append({
            "id": l.id,
            "internship_id": l.internship_id,
            "status": l.status,
            "staff_id": l.staff_id
        })
    return jsonify(result), 200
