import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Staff, Student, Shotlist, Position
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    create_employer,
    update_employer,
    create_staff,
    update_staff,
    create_student,
    update_student,
    create_position,
    update_position,
    add_student,
    respond
    view_student_listing,
    view_response,
    create_listing
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

# Employer - Unit tests

    def test_create_employer(self):
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        assert employer.username = "john"

    def test_update_username(self):
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        updatedemployer = update_employer(employer.id, "john_updated", "ACE Tech", "IT", "2223456", "john@acetech.com")
        assert updatedemployer.username = "john_updated"

# Staff - Unit Tests
    def create_staff(self):
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        assert staff.username = "jill"

    def update_staff(self):
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        updatedstaff = update_staff(staff.id, "jill_updated", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        assert updatedstaff.username = "jill_updated"

# Student - Unit Tests
    def create_student(self):
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        assert student.username = "rose"

    def update_student(self):
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        updatedstudent = update_student(student.id, "rose_updated", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        assert student.username = "rose_updated"

# Position - Unit Tests
    def create_position(self):
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        assert position.title = "IT Assistant"

    def update_position(self):
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        updatedposition = update_position(position.id, "IT Assistant UPDATED", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id
        assert updatedposition.title = "IT Assistant UPDATED"

# Shortlisting / Response - Unit Tests
    def test_add_student_listing(self):
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        listing = add_student(staff.id, student.id, position.id)
        assert listing.status == "Pending"

    def test_respond(self):
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        listing = add_student(staff.id, student.id, position.id)
        reponse = respond(employer.id, listing.id, "Accpeted")
        assert response.status = "Accepted"

    def test_view_student_listing(self):
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        add_student(staff.id, student.id, position.id)
        result = view_student_listing(student.id)
        assert isinstance(result, list)
        assert len(results) > 0

    def test_view_accepted(self)
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        listing = create_listing(position.id, student.id, staff.id)
        respond(employer.id, listing.id, "Accepted")
        accepted = view_response(student.id, "Accepted")
        assert isinstance(accepted, list)
        assert len(accepted) > 0

    def test_view_rejected(self)
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        listing = create_listing(position.id, student.id, staff.id)
        respond(employer.id, listing.id, "Accepted")
        rejected = view_response(student.id, "Rejected")
        assert isinstance(rejected, list)
        assert len(rejected) > 0

    def test_view_pending(self)
        staff = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        student = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        employer = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        listing = create_listing(position.id, student.id, staff.id)
        respond(employer.id, listing.id, "Pending")
        pending = view_response(student.id, "Pending")
        assert isinstance(pending, list)
        assert len(pending) > 0

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
        

