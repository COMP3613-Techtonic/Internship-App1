from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user


from App.controllers import (
  get_all_staff,
  get_staff,
  create_staff,
  update_staff,
  add_student,
view_staff_listing
)

staff_views = Blueprint('staff', __name__, url_prefix='/staff')


# @staff_views.route('/staff', methods=['GET']) # list all staff

# @staff_views.route("/staff",methods=['POST']) # create staff

# @staff_views.route('/staff/<int:staff_id>', methods=['PUT']) # update staff

# @staff_views.route('/staff/<int:staff_id>/add-students', methods=['POST']) # add student to an already existing short list ?


