from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import (
    create_employer,
    get_employer,
    update_employer,
    view_positions,
    respond,
    view_shortlist)

employer_views = Blueprint('employer', __name__, url_prefix='/employer')

# @employer_views.route('/employer', methods=['POST'])  # create employer
# @employer_views.route('/employer',methods=['GET'])  # get employer details
# @employer_views.route('/employer/<int:emp_id>', methods=['PUT'])  # update employer details
# @employer_views.route('/employer/<int:emp_id>/positions', methods=['GET'])  # view all internship positions created by employer X
# @employer_views.route('/employer/<int:emp_id>/shortlist', methods=['GET'])  # view shortlist of students for employer X
# @employer_views.route('/employer/<int:emp_id>/respond', methods=['POST'])  # respond to a listing   / would this be PUT ?




