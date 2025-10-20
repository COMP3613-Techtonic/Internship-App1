import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
from App.controllers.employer import *
from App.controllers.staff import *
from App.controllers.student import *
from App.controllers.position import *
from App.controllers.shortlist import *

# This commands file allow you to create convenient CLI commands for testing controllers
#fr

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)

#Employer commands
employer_cli = AppGroup('employer', help="Employer object commands")

@employer_cli.command("create", help='Creates an employer')
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.option("--company", prompt="Enter company:", default="")
@click.option("--department", prompt="Enter department", default="")
@click.option("--telephone", prompt="Enter telephone number", default="")
@click.option("--email", prompt="Enter email", default="")
def create_employer_command(username, password, company, department, telephone, email):
    employer = create_employer(username, password, company, department, telephone, email)
    print (f'Employer {username} created with id {employer.id}')

@employer_cli.command("update", help="Updates an employer")
@click.argument("employer_id", default="1")
def update_employer_command(employer_id):
    emp = get_employer(employer_id)
    if not emp:
        print(f'Employer not found')
    else:
        username = click.prompt("Enter username", default="")
        company = click.prompt("Enter company", default="")
        department = click.prompt("Enter department", default="")
        telephone = click.prompt("Enter telephone number", default="")
        email = click.prompt("Enter email", default="")
        employer = update_employer(employer_id, username, company, department, telephone, email)
        print (f'Employer {username} updated!')
        print(employer)

@employer_cli.command("list-all", help="List all employers")
def get_all_employers_command():
    employers = get_all_employers()
    if not employers:
        print(f'No employers found')
    for employer in employers:
        print(employer)

@employer_cli.command("view-positions", help="Lists internship positions listed by employer")
@click.argument("employer_id", default="1")
def view_positions_command(employer_id):
    positions = view_positions(employer_id)
    if isinstance(positions, str):
        print(positions)
    else:
        for position in positions:
            print(position)

@employer_cli.command("view-shortlist", help="Lists employer's student shortlist")
@click.argument("employer_id", default="1")
def view_shortlist_command(employer_id):
    list = view_shortlist(employer_id)
    if isinstance(list, str):
        print(list)
    else:
        for listing in list:
            print(list)

@employer_cli.command("respond", help="Respond to a student listing")
@click.argument("employer_id", default="1")
@click.option("--listing_id", prompt="Enter intership ID:", default="1")
@click.option("--response", prompt="Enter response:", default="Accepted/Rejected")
def respond_command(employer_id, listing_id, response):
    if response not in ["Accepted", "Rejected"]:
        print(f'Invalid response: Student can either be Accepted OR Rejected')
    else:
        print(respond(employer_id, listing_id, response))

app.cli.add_command(employer_cli)

#Staff commands
staff_cli = AppGroup('staff', help="Staff object commands")

@staff_cli.command("create", help="Create a staff member")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.option("--university", prompt="Enter university", default="")
@click.option("--department", prompt="Enter department", default="")
@click.option("--telephone", prompt="Enter telephone", default="")
@click.option("--email", prompt="Enter email", default="")
def create_staff_command(username, password, university, department, telephone, email):
    staff = create_staff(username, password, university, department, telephone, email)
    print (f'Staff {username} created with id {staff.id}!')

@staff_cli.command("update", help="Updates a staff member")
@click.argument("staff_id", default="1")
def update_staff_command(staff_id):
    staff = get_staff(staff_id)
    if not staff:
        print(f'Staff member not found')
    else:
        username = click.prompt("Enter username", default="")
        university = click.prompt("Enter university", default="")
        department = click.prompt("Enter department", default="")
        telephone = click.prompt("Enter telephone number", default="")
        email = click.prompt("Enter email", default="")
        staff = update_staff(staff_id, username, university, department, telephone, email)
        print (f'Staff {username} updated!')
        print(staff)

@staff_cli.command("list-all", help="List all staff")
def get_all_staff_command():
    staff = get_all_staff()
    if not staff:
        print(f'No staff found')
    for s in staff:
        print(s)

@staff_cli.command("add-student", help="Create a student listing")
@click.argument("staff_id", default="1")
@click.argument("student_id", default="1")
@click.argument("position_id", default="1")
def add_student_command(staff_id, student_id, position_id):
    result = add_student(staff_id, student_id, position_id)
    if isinstance(result, str):
        print(result)
    else:
        print(f'Listing ID: {result.id} created with Student {student_id} for internship position {position_id} by staff member {staff_id}')

@staff_cli.command("view-list", help="View listings associated with staff member")
@click.option("--staff_id", prompt="Enter staffID:", default="1")
def view_staff_listing_command(staff_id):
    list = view_staff_listing(staff_id)
    if isinstance(list, str):
        print(list)
    else:
        for listing in list:
            print (listing)

app.cli.add_command(staff_cli)

#Student commands
student_cli = AppGroup('student', help="Student object commands")

@student_cli.command("create", help="Create a student")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
@click.option("--university", prompt="Enter university:", default="")
@click.option("--major", prompt="Enter major", default="")
@click.option("--year", prompt="Enter year of degree", default="1")
@click.option("--telephone", prompt="Enter telephone", default="")
@click.option("--email", prompt="Enter email", default="")
def create_student_command(username, password, university, major, year, telephone, email):
    student = create_student(username, password, university, major, year, telephone, email)
    print (f'Student {username} created with id {student.id}!')

@student_cli.command("update", help="Update student")
@click.argument("student_id", default="1")
def update_student_command(student_id):
    student = get_student(student_id)
    if not student:
        print(f'Student not found')
    else:
        username = click.prompt("Enter username:", default="")
        university = click.prompt("Enter university:", default="")
        major = click.prompt("Enter major:", default="")
        year = click.prompt("Enter year of degree:", default="1")
        telephone = click.prompt("Enter telephone:", default="")
        email = click.prompt("Enter email:", default="")
        student = update_student(student_id, username, university, major, year, telephone, email)
        print (f'Student {username} updated!')
        print(student)

@student_cli.command("list-all", help="List all students")
def get_all_students_command():
    students = get_all_students()
    if not students:
        print(f'No students found')
    for student in students:
        print(student)

@student_cli.command("view-shortlist", help="View student shortlist")
@click.argument("student_id", default="1")
def view_student_listing_command(student_id):
    list = view_student_listing(student_id)
    if isinstance(list, str):
        print(list)
    else:
        for listing in list:
            print (listing)

@student_cli.command("view-responses", help="View employer responses")
@click.argument("student_id", default="1")
@click.option("--status", prompt="Enter status to search:", default="Accepted")
def view_response_command(student_id, status):
    list = view_response(student_id, status)
    if isinstance(list, str):
        print(list)
    else:
        for listing in list:
            print (listing)

app.cli.add_command(student_cli)

#Position commands
position_cli = AppGroup('position', help="Internship position object commands")

@position_cli.command("create", help="Create an internship position")
@click.option("--title", prompt="Enter title:", default="title")
@click.option("--description", prompt="Enter description", default="")
@click.option("--requirements", prompt="Enter requirements", default="")
@click.option("--location", prompt="Enter location", default="")
@click.option("--employer_id", prompt="Enter employer id:", default="1")
def create_position_command(title, description, requirements, location, employer_id):
    pos = create_position(title, description, requirements, location, employer_id)
    print (f'Internship position {pos.id} created!')

@position_cli.command("update", help="Update position")
@click.argument("position_id", default="1")
def update_position_command(position_id):
    pos = get_position(position_id)
    if not pos:
        print(f'Internship position not found')
    else:
        emp_id = click.prompt("Enter employer ID:", default="1")
        description = click.prompt("Enter description", default="")
        requirements = click.prompt("Enter requirements", default="")
        location = click.prompt("Enter location", default="")
        pos = update_position(position_id, description, requirements, location, emp_id)
        print (f'Internship position {pos.id} updated!')
        print(pos)

@position_cli.command("view-all", help="List all posistions")
def get_all_positions_command():
    positions = get_all_positions()
    if not positions:
        print(f'No posistions available')
    else:
        for position in positions:
            print(position)

app.cli.add_command(position_cli)

#Shortlist commands
shortlist_cli = AppGroup('shortlist', help="Shortlist object commands")

@shortlist_cli.command("create", help="Create a listing")
@click.argument("internship_id", default="1")
@click.argument("student_id", default="1")
@click.argument("staff_id", default="1")
def create_listing_command(internship_id, student_id, staff_id):
    create_listing(internship_id, student_id, staff_id)
    print (f'Internship {internship_id}: Student {student_id} added to shortlist by staff {staff_id}')

@shortlist_cli.command("update", help="Update internship position")
@click.argument("listing_id", default="1")
def update_listing_command(listing_id):
    listing = get_listing(listing_id)
    if not listing:
        print(f'Listing not found')
    else:
        internship_id = click.prompt("Enter internship id", default="1")
        student_id = click.prompt("Enter student id", default="1")
        staff_id = click.prompt("Enter staff id", default="1")
        listing = update_listing(listing_id, internship_id, student_id, staff_id)
        print(f'Listing {listing.id} updated!')
        print(listing)

@shortlist_cli.command("view-all", help="View all listings")
def get_all_listings_command():
    listings = get_all_listings()
    if not listings:
        print(f'No listings available')
    else:
        for listing in listings:
            print(listing)

app.cli.add_command(shortlist_cli)
