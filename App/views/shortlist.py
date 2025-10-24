"""
Shortlist endpoints.

Routes:
- POST   /shortlists           -> create a shortlist listing (auth: staff)
- GET    /shortlists           -> list all shortlist entries (admin/dev)
- GET    /shortlists/position/<int:position_id>  -> shortlist for a position (auth)
- GET    /shortlists/student/<int:student_id>    -> shortlist entries for a student (auth)
- PUT    /shortlists/<int:listing_id>            -> update a listing (auth)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    create_listing,
    get_all_listings,
    get_listing,
    get_employer_shortlist,
    get_student_shortlist,
    get_staff_shortlist,
    update_listing
)

shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')


@shortlist_views.route('/shortlists', methods=['POST'])
@jwt_required()
def create_shortlist_route():
    """
    Create a shortlist entry.
    Body JSON: { internship_id, student_id, staff_id }
    """
    data = request.get_json() or {}
    required = ['internship_id', 'student_id', 'staff_id']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    listing = create_listing(data['internship_id'], data['student_id'], data['staff_id'])
    return jsonify({
        "message": "Listing created",
        "listing_id": listing.id
    }), 201


@shortlist_views.route('/shortlists', methods=['GET'])
def list_all_shortlists_route():
    """
    Return all shortlist entries (useful for admin/testing).
    """
    listings = get_all_listings()
    result = []
    for l in listings:
        result.append({
            "id": l.id,
            "internship_id": l.internship_id,
            "student_id": l.student_id,
            "staff_id": l.staff_id,
            "status": l.status
        })
    return jsonify(result), 200


@shortlist_views.route('/shortlists/position/<int:position_id>', methods=['GET'])
@jwt_required()
def get_position_shortlists_route(position_id):
    """
    Get shortlist entries for a specific position (employer view).
    """
    employer_id = get_jwt_identity()
    
    # Get all shortlists for this employer
    listings = get_employer_shortlist(employer_id)
    
    # Filter by the specific position_id
    position_listings = [l for l in listings if l.internship_id == position_id]
    
    if not position_listings:
        return jsonify({"message": "No shortlist entries found"}), 404
    
    result = []
    for l in position_listings:
        result.append({
            "id": l.id,
            "internship_id": l.internship_id,
            "student_id": l.student_id,
            "staff_id": l.staff_id,
            "status": l.status
        })
    
    return jsonify(result), 200


@shortlist_views.route('/shortlists/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_shortlists_route(student_id):
    """
    Student view of their shortlist entries.
    """
    listings = get_student_shortlist(student_id)
    if not listings:
        return jsonify({"message": "No listings available"}), 404
    result = []
    for l in listings:
        result.append({
            "id": l.id,
            "internship_id": l.internship_id,
            "student_id": l.student_id,
            "staff_id": l.staff_id,
            "status": l.status
        })
    return jsonify(result), 200


@shortlist_views.route('/shortlists/<int:listing_id>', methods=['PUT'])
@jwt_required()
def update_shortlist_route(listing_id):
    """
    Update a listing. Provide fields to update (internship_id, student_id, staff_id).
    """
    data = request.get_json() or {}
    internship_id = data.get('internship_id')
    student_id = data.get('student_id')
    staff_id = data.get('staff_id')

    updated = update_listing(listing_id, internship_id or None, student_id or None, staff_id or None)
    if isinstance(updated, str):
        return jsonify({"error": updated}), 404
    return jsonify({
        "message": "Listing updated",
        "listing": {
            "id": updated.id,
            "internship_id": updated.internship_id,
            "student_id": updated.student_id,
            "staff_id": updated.staff_id,
            "status": updated.status
        }
    }), 200
