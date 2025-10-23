import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Staff, Student, Shortlist, Position
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    create_employer, update_employer, get_employer, get_employer_by_username,
    create_staff, update_staff, get_staff, get_staff_by_username,
    create_student, update_student, get_student, get_student_by_username,
    create_position, update_position, get_position,
    add_student, get_listing,
    respond,
    view_student_listing,
    view_response,
    create_listing,
    get_employer_by_username,
    get_staff_by_username,
    get_student_by_username,
    
)


LOGGER = logging.getLogger(__name__)

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()
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
        user = User("bob", "bobpass")
        self.assertNotEqual( user.password,"bobpass")

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

# Employer - Unit tests
class EmployerUnitTests(unittest.TestCase):

    def test_new_employer(self):
        employer = Employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        assert employer.username == "john"

# Staff - Unit Tests
class StaffUnitTests(unittest.TestCase):
    def test_new_staff(self):
        staff = Staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        assert staff.username == "jill"

# Student - Unit Tests
class StudentUnitTests(unittest.TestCase):
    def test_new_student(self):
        student = Student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        assert student.username == "rose"


# Position - Unit Tests
class PositionUnitTests(unittest.TestCase):
    def test_new_position(self):
        employer = Employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        position = Position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        assert position.title == "IT Assistant"


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

def test_00_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_01_create_user(self):  
        user = create_user("rick", "bobpass")    
        assert user.username == "rick"

    def test_02_get_all_users_json(self):
        user2=create_user("morty", "mortypass")
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"},{"id":2, "username":"rick"}, {"id":3, "username":"morty"}], users_json)

    # Tests data changes in the database
    def test_03_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

    # Ensures employer record in the database has the correct values
    def test_04_create_employer(self):
        john = create_employer("john", "johnpass", "ACE Tech", "IT", "2223456", "john@acetech.com")
        user = get_employer_by_username("john")
        assert user.username == john.username

    # Ensures employer record is correctly updated with new data using username
    def test_05_update_employer(self):
        employer = get_employer_by_username("john")
        updatedemployer = update_employer(employer.id, "john_updated", "ACE Tech", "IT", "2223456", "john@acetech.com")
        assert updatedemployer.username == "john_updated"

    # Ensures staff record in the database has the correct values
    def test_06_create_staff(self):
        jill = create_staff("jill", "jillpass", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        user = get_staff_by_username("jill")
        assert user.username == jill.username

    # Ensures staff record is correctly updated with new data using username
    def test_07_update_staff(self):
        staff = get_staff_by_username("jill")
        updatedstaff = update_staff(staff.id, "jill_updated", "UWI", "DCIT", "3334456", "jill@uwistaff.edu")
        assert updatedstaff.username == "jill_updated"

    # Ensures student record in the database has the correct values
    def test_08_create_student(self):
        rose = create_student("rose", "rosepass", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        user = get_student_by_username("rose")
        assert user.username == rose.username

    # Ensures student record is correctly updated with new data using username
    def test_09_update_student(self):
        rose = get_student_by_username("rose")
        updatedstudent = update_student(rose.id, "rose_updated", "UWI", "IT", 2, "1234567", "rose@uwi.edu")
        assert updatedstudent.username == "rose_updated"

    # Ensures position record in the database has the correct values
    def test_10_create_position(self):
        employer = get_employer_by_username("john_updated")
        internship = create_position("IT Assistant", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", employer.id)
        position = get_position(internship.id)
        assert position.title == "IT Assistant"

    # Ensures position record is correctly updated with new data using position title
    def test_11_update_position(self):
        internship = get_position(1)
        updatedposition = update_position(internship.id, "IT Assistant UPDATED", "Assist wih service requests", "Level 2 IT degree or equivalent", "POS", internship.employer_id)
        assert updatedposition.title == "IT Assistant UPDATED"
    
    # Ensures student is added to shortlist for a specified position by staff, with default status “Pending”
    def test_12_add_student_listing(self):
        staff = get_staff_by_username("jill_updated")
        student = get_student_by_username("rose_updated")
        position = get_position(1)
        listing = add_student(staff.id, student.id, position.id)
        assert listing.status == "Pending"

    # Ensures employer’s response to specified listing is correctly updated
    def test_13_employer_response(self):
        employer = get_employer_by_username("john_updated")
        listing = get_listing(1)
        response = respond(employer.id, listing.id, "Accepted")
        assert response.status == "Accepted"

    # Ensures list of student shortlist is available
    def test_14_view_student_listing(self):
        student = get_student_by_username("rose_updated")
        result = view_student_listing(student.id)
        assert isinstance(result, list)
        assert len(result) > 0

    # Ensures list of pending / accepted / rejected positions are available
    def test_15_view_response(self):
        student = get_student_by_username("rose_updated")
        employer = get_employer_by_username("john_updated")
        listing = get_listing(1)
        respond(employer.id, listing.id, "Pending")
        pending = view_response(student.id, "Pending")
        assert isinstance(pending, list)
        assert len(pending) > 0
        
        respond(employer.id, listing.id, "Accepted")
        accepted = view_response(student.id, "Accepted")
        assert isinstance(accepted, list)
        assert len(accepted) > 0

        respond(employer.id, listing.id, "Rejected")
        rejected = view_response(student.id, "Rejected")
        assert isinstance(rejected, list)
        assert len(rejected) > 0