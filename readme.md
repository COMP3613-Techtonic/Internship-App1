![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```

The following are the commands for Employer:

```python
#inside wsgi.py

#Creates a new employer with username, password, company name, department and contact info
@employer_cli.command("create", help="Creates an employer")
...
def create_employer_command(username, password, company, department, telephone, email):
    ...
    employer = create_employer(username, password, company, department, telephone, email)
    print (f'Employer {username} created with id {employer.id}')

#Updates an employer's details such as username, company details, and contact info
#The command first checks that the employer exists and then proceeds to prompt the user for updated data
#If the employer does not exist then an error message is shown
@employer_cli.command("update", help="Updates an employer")
...
def update_employer_command(employer_id):
    emp = get_employer(employer_id)
    if not emp:
        print(f'Employer not found')
    else:
        ...
        employer = update_employer(employer_id, username, company, department, telephone, email)
        print (f'Employer {username} updated!')
        print(employer)

#Displays all the employers in the system or an error message if there is not any employers
@employer_cli.command("list-all", help="List all employers")
...
def get_all_employers_command():
    ...

#TDisplays all internship positions created by a specified employer
@employer_cli.command("view-positions", help="Lists internship positions listed by employer")
...
def view_positions_command(employer_id):
    ...

#Displays all student shortlist entries for a specified employer
@employer_cli.command("view-shortlist", help="Lists employer's student shortlist")
...
def view_shortlist_command(employer_id):
    ...

#Allows an employer to accept or reject a student from their shortlist. It only allows"Accepted" and "Rejected"
@employer_cli.command("respond", help="Respond to a student listing")
...
def respond_command(employer_id, listing_id, response):
    ...
```

```bash
#Example:

$ flask employer create bob bobpass --company="ACE Tech" --department="Computer Science" --telephone="123-4567" --email="bob@acetech.com"

$ flask employer update 2
#The system then prompts the user for updated data once employer with id 2 exists

$ flask employer list-all

$ flask employer view-positions 2

$ flask employer view-shortlist 2

$ flask employer respond 2 --listing_id=3 --response="Accepted"
```

The following are the commands for Staff:

```python
#Creates a new staff member with username, password, university, department, and contact info
@staff_cli.command("create", help="Create a staff member")
...
def create_staff_command(username, password, university, department, telephone, email):
    ...
    staff = create_staff(username, password, university, department, telephone, email)
    print(f'Staff {username} created with id {staff.id}!')

#Updates a staff member's details
#The command first checks that the staff member exists and then proceeds to prompt the user for updated data
#If the staff member does not exist then an error message is shown
@staff_cli.command("update", help="Updates a staff member")
...
def update_staff_command(staff_id):
    staff = get_staff(staff_id)
    if not staff:
        print(f'Staff member not found')
    else:
    ...
    staff = update_staff(staff_id, username, university, department, telephone, email)
        print (f'Staff {username} updated!')
        print(staff)

#Lists all staff members in the system or error message if no staff found
@staff_cli.command("list-all", help="List all staff")
...
def get_all_staff_command():
    ...

#Adds a student to a specific internship position shortlist
@staff_cli.command("add-student", help="Create a student listing")
...
def add_student_command(staff_id, student_id, position_id):
    ...

#Displays all listings associated with a specified staff member
@staff_cli.command("view-list", help="View listings associated with staff member")
...
def view_staff_listing_command(staff_id):
    ...
```

```bash
#Example:

$ flask staff create lisa lisapass --university="UWI" --department="IT" --telephone="555-1234" --email="lisa@uwi.com"

$ flask staff update 3
#Prompts to update staff data once staff with id 3 exists

$ flask staff list-all

$ flask staff add-student 1 3 2

$ flask staff view-list --staff_id=1

```


The following are the commands for Student:

```python

#Creates a new student
@student_cli.command("create", help="Create a student")
...
def create_student_command(username, password, university, major, year, telephone, email):
    ...

#Updates student data
#The command first checks that the student exists and then proceeds to prompt the user for updated data
#If the student does not exist then an error message is shown
@student_cli.command("update", help="Update student")
...
def update_student_command(student_id):
    student = get_student(student_id)
    if not student:
        print(f'Student not found')
    else:
        ...
        student = update_student(student_id, username, university, major, year, telephone, email)
        print (f'Student {username} updated!')
        print(student)

#Lists all students
@student_cli.command("list-all", help="List all students")
...
def get_all_students_command():
    ...

#Displays a student's shortlisted internship positions
@student_cli.command("view-shortlist", help="View student shortlist")
...
def view_student_listing_command(student_id):
    ...

#Displays employer's responses to student. Internship shortlist status can eithe be "Pending", "Accepted" or "Rejected"
@student_cli.command("view-responses", help="View employer responses")
...
def view_response_command(student_id, status):
    ...

```

```bash
#Example:

$ flask student create cait caitpass --university="UWI" --major="Computer Science" --year=3 --telephone="356-7646" --email="cait@uwi.com"

$ flask student update 7
#Prompts to update student info once the student with id 7 exists

$ flask student list-all

$ flask student view-shortlist 7

$ flask student view-responses 7 --status="Accepted"
```

The following are the commands for Position (the internship positions created by employers)

```python
#Creates a new internship position
@position_cli.command("create", help="Create an internship position")
...
def create_position_command(title, description, requirements, location, employer_id):
    ...

#Update an internship position
#The command first checks that the position exists and then proceeds to prompt the user for updated data
#If the position does not exist then an error message is shown
@position_cli.command("update", help="Update position")
...
def update_position_command(position_id):
    pos = get_position(position_id)
    if not pos:
        print(f'Internship position not found')
    else:
        ...
        pos = update_position(position_id, description, requirements, location, emp_id)
        print (f'Internship position {pos.id} updated!')
        print(pos)

#Lists all internship positions
@position_cli.command("view-all", help="List all positions")
...
def get_all_positions_command():
    ...
```

```bash
#Example:

$ flask position create --title="Sales Rep" --description="Aid in front desk services" --requirements="Marketing, year1+" --location="POS" --employer_id=5

$ flask position update 2
#Prompts to update internship details once the internship position with id 2 exists

$ flask position view-all
```


The following commands are for Shortlist:

```python
#Creates a listing (a shortlist entry) for student a specified internship position, done by a staff member
@shortlist_cli.command("create", help="Create a listing")
...
def create_listing_command(internship_id, student_id, staff_id):
    ...

#Updates a shortlist record
#The command first checks that the listing exists and then proceeds to prompt the user for updated data
#If the listing does not exist then an error message is shown
@shortlist_cli.command("update", help="Update internship position")
...
def update_listing_command(listing_id):
    listing = get_listing(listing_id)
    if not listing:
        print(f'Listing not found')
    else:
        ...
        listing = update_listing(listing_id, internship_id, student_id, staff_id)
        print(f'Listing {listing.id} updated!')
        print(listing)

#Displays all shortlists
@shortlist_cli.command("view-all", help="View all listings")
...
def get_all_listings_command():
    ...
```

```bash
#Example:

$ flask shortlist create 1 4 3

$ flask shortlist update 1
#Prompts to update internship_id, student_id, staff_id once the listing with id 1 exists

$ flask shortlist view-all
```

# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
