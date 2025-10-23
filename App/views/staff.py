"""
Staff-related endpoints.

Routes (blueprint url_prefix='/staff'):
- POST   /staff/                 -> create staff (public)
- GET    /staff/                 -> list all staff (public/admin)
- POST   /staff/<int:staff_id>/add-student  -> add a student to a position's shortlist (auth: staff)
- GET    /staff/<int:staff_id>/listings     -> view listings for a staff member (auth)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    create_staff,
    get_all_staff,
    add_student,
    view_staff_listing,
    get_staff
)

staff_views = Blueprint('staff', __name__, url_prefix='/staff')


@staff_views.route('/', methods=['POST'])
def create_staff_route():
    """
    Create a staff account.
    Body JSON: { username, password, university, department, telephone, email }
    """
    data = request.get_json() or {}
    required = ['username', 'password', 'university', 'department', 'telephone', 'email']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    staff = create_staff(
        data['username'],
        data['password'],
        data['university'],
        data['department'],
        data['telephone'],
        data['email']
    )
    return jsonify({"message": "Staff created", "id": staff.id}), 201


@staff_views.route('/', methods=['GET'])
def list_staff_route():
    staff = get_all_staff()
    result = []
    for s in staff:
        result.append({
            "id": s.id,
            "username": s.username,
            "university": getattr(s, "university", None)
        })
    return jsonify(result), 200


@staff_views.route('/<int:staff_id>/add-student', methods=['POST'])
@jwt_required()
def staff_add_student_route(staff_id):
    """
    Staff adds a student to a position's shortlist.
    Body JSON: { "student_id": <int>, "position_id": <int> }
    """
    data = request.get_json() or {}
    student_id = data.get('student_id')
    position_id = data.get('position_id')
    if not student_id or not position_id:
        return jsonify({"error": "student_id and position_id required"}), 400

    result = add_student(staff_id, student_id, position_id)
    if isinstance(result, str):
        return jsonify({"error": result}), 400
    return jsonify({
        "message": "Student added to shortlist",
        "listing_id": result.id
    }), 201


@staff_views.route('/<int:staff_id>/listings', methods=['GET'])
@jwt_required()
def staff_listings_route(staff_id):
    """
    View listings associated with a staff member.
    """
    listings = view_staff_listing(staff_id)
    if isinstance(listings, str):
        return jsonify({"message": listings}), 404

    result = []
    for l in listings:
        result.append({
            "id": l.id,
            "internship_id": l.internship_id,
            "student_id": l.student_id,
            "status": l.status
        })
    return jsonify(result), 200



