from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import(
    create_listing,
    get_listing,
    get_all_listings,
    get_employer_shortlist,
    get_student_shortlist,
    get_staff_shortlist,
    update_listing
)

shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')

# @shortlist_views.route('/shortlists', methods=['GET'])  # View all listings


# @shortlist_views.route('/shortlists', methods=['POST'])  # Create a new listing

# @shortlist_views.route('/shortlists/<int:list_id>', methods=['PUT'])  # Update a listing