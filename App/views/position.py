from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user


from App.controllers import (
    get_all_positions,
    get_position_by_id,
    create_position,
    update_position,
)
position_views = Blueprint('position_views', __name__, template_folder='../templates')


# @position_views.route('/positions', methods=['GET']) #view all positions

# @position_views.route('/positions', methods=['POST']) # create a new position

# @position_views.route('/positions/<int:position_id>', methods=['PUT']) # update position