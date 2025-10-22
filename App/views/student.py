from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from App.controllers import (
    get_all_students,
    get_student,
    create_student,
    update_student,
view_student_listing,
view_response)

student_view=Blueprint('student',__name__,prefix='/student')

# @student_view.route('/students', methods=['GET']) # list all students
# @student_view.route('/students',methods=['POST']) # create student
# @student_view.route('/students/<int:student_id>', methods=['PUT']) # update student
# @student_view.route('/students/<int:student_id>/shortlist', methods=['GET']) # view student listing
# @student_view.route('/students/<int:student_id>/response', methods=['GET']) # view student response
