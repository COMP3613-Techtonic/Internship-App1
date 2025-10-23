"""
Employer-related REST endpoints.

Routes (blueprint url_prefix='/employer'):
- POST   /employer/                 -> create employer (public)
- GET    /employer/                 -> list all employers
- GET    /employer/<int:employer_id>/positions   -> list positions for an employer (auth)
- GET    /employer/<int:employer_id>/shortlist   -> list shortlist entries for an employer (auth)
- POST   /employer/respond          -> employer responds to a shortlist entry (auth)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    create_employer,
    get_all_employers,
    view_positions,
    view_shortlist,
    respond,
    get_employer
)

employer_views = Blueprint('employer', __name__, url_prefix='/employer')


@employer_views.route('/', methods=['POST'])
def create_employer_route():
    """
    Create a new employer account.
    Body JSON: { username, password, company, department, telephone, email }
    """
    data = request.get_json() or {}
    required = ['username', 'password', 'company', 'department', 'telephone', 'email']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    emp = create_employer(
        data['username'],
        data['password'],
        data['company'],
        data['department'],
        data['telephone'],
        data['email']
    )
    return jsonify({"message": "Employer created", "id": emp.id}), 201


@employer_views.route('/', methods=['GET'])
def list_employers_route():
    """
    Return a simple list of all employers (public).
    """
    employers = get_all_employers()
    result = []
    for e in employers:
        result.append({
            "id": e.id,
            "username": e.username,
            "company": getattr(e, "company", None)
        })
    return jsonify(result), 200


@employer_views.route('/<int:employer_id>/positions', methods=['GET'])
@jwt_required()
def employer_positions_route(employer_id):
    """
    Return all positions owned by the specified employer.
    Protected route (requires JWT).
    """
    positions = view_positions(employer_id)
    if isinstance(positions, str):
        return jsonify({"error": positions}), 404

    result = []
    for p in positions:
        result.append({
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "requirements": p.requirements,
            "location": p.location,
            "employer_id": p.employer_id
        })
    return jsonify(result), 200


@employer_views.route('/<int:employer_id>/shortlist', methods=['GET'])
@jwt_required()
def employer_shortlist_route(employer_id):
    """
    Return shortlist entries for all positions of an employer.
    Protected route.
    """
    sl = view_shortlist(employer_id)
    if isinstance(sl, str):
        return jsonify({"error": sl}), 404

    result = []
    for entry in sl:
        result.append({
            "id": entry.id,
            "internship_id": entry.internship_id,
            "student_id": entry.student_id,
            "staff_id": entry.staff_id,
            "status": entry.status
        })
    return jsonify(result), 200


@employer_views.route('/respond', methods=['POST'])
@jwt_required()
def employer_respond_route():
    """
    Employer responds to a shortlist listing.
    Body JSON: { "listing_id": <int>, "response": "Accepted" | "Rejected" }
    The employer_id is taken from the JWT identity (current user).
    """
    data = request.get_json() or {}
    listing_id = data.get("listing_id")
    response_text = data.get("response")
    if not listing_id or not response_text:
        return jsonify({"error": "listing_id and response required"}), 400

    try:
        employer_id = int(get_jwt_identity())
    except Exception:
        return jsonify({"error": "Invalid token identity"}), 401

    result = respond(employer_id, listing_id, response_text)
    if isinstance(result, str):
        return jsonify({"error": result}), 400

    return jsonify({
        "message": "Response recorded",
        "listing": {
            "id": result.id,
            "internship_id": result.internship_id,
            "student_id": result.student_id,
            "status": result.status
        }
    }), 200





