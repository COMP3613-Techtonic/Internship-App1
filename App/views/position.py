"""
Position (internship) endpoints.

Routes (no url_prefix set in your file, so endpoints will be registered at root):
- POST   /positions        -> create position (auth: employer)
- GET    /positions        -> list all positions (public)
- GET    /positions/<id>   -> get a single position (public)
- PUT    /positions/<id>   -> update position (auth: employer)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    create_position,
    get_all_positions,
    get_position,
    update_position
)
position_views = Blueprint('position_views', __name__, template_folder='../templates', url_prefix='/api')



@position_views.route('/positions', methods=['POST'])
@jwt_required()
def create_position_route():
    """
    Create a new internship position.
    Body JSON: { title, description, requirements, location }
    employer_id is taken from JWT identity.
    """
    data = request.get_json() or {}
    required = ['title', 'description', 'requirements', 'location']
    if not all(k in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    try:
        employer_id = int(get_jwt_identity())
    except Exception:
        return jsonify({"error": "Invalid token identity"}), 401

    pos = create_position(
        data['title'],
        data['description'],
        data['requirements'],
        data['location'],
        employer_id
    )
    return jsonify({
        "message": "Position created",
        "position_id": pos.id
    }), 201


@position_views.route('/positions', methods=['GET'])
def list_positions_route():
    """
    List all positions (public).
    """
    positions = get_all_positions()
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


@position_views.route('/positions/<int:position_id>', methods=['GET'])
def get_position_route(position_id):
    """
    Return a single position by id.
    """
    pos = get_position(position_id)
    if not pos:
        return jsonify({"error": "Position not found"}), 404
    return jsonify({
        "id": pos.id,
        "title": pos.title,
        "description": pos.description,
        "requirements": pos.requirements,
        "location": pos.location,
        "employer_id": pos.employer_id
    }), 200


@position_views.route('/positions/<int:position_id>', methods=['PUT'])
@jwt_required()
def update_position_route(position_id):
    """
    Update a position. Only employer owning the position should do this in practice.
    Body JSON: fields to update (title, description, requirements, location)
    """
    data = request.get_json() or {}
    pos = get_position(position_id)
    if not pos:
        return jsonify({"error": "Position not found"}), 404

    # For now we accept whatever is provided; controllers will update fields
    title = data.get('title', pos.title)
    description = data.get('description', pos.description)
    requirements = data.get('requirements', pos.requirements)
    location = data.get('location', pos.location)

    updated = update_position(position_id, title, description, requirements, location, pos.employer_id)
    return jsonify({"message": "Position updated", "position_id": updated.id}), 200
