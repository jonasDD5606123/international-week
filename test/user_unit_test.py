import pytest
import random
import string
from database_context import DatabaseContext
from model.user import User
from model.drone import Drone
from model.locatie import Locatie

# Fixture to setup the database connection for tests
@pytest.fixture
def test_db():
    """Fixture to setup and teardown the database connection."""
    dc = DatabaseContext('test/test.db')
    conn = dc.getDbConn()
    yield conn  # Yield the connection to the test
    conn.close()  # Ensure connection is closed after tests.

# Fixture to create a user with a unique name for each test
@pytest.fixture
def test_user(test_db):
    """Fixture to create a user with a unique name for testing."""
    unique_name = f"TestUser_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"  # Generate a unique user name
    user = User(naam=unique_name, rol="admin")
    user.create()  # Insert the user into the database
    return user

def test_create_user(test_db):
    """Test creating a new user with a unique name."""
    unique_name = f"NewUser_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"  # Generate a unique user name
    user = User(naam=unique_name, rol="user")
    user.create()  # Insert the user into the database

    assert user.id is not None  # Ensure the user has been created and ID is assigned

    # Verify the user was correctly inserted into the database
    fetched_user = User.by_id(user.id)
    assert fetched_user.id == user.id
    assert fetched_user.naam == user.naam
    assert fetched_user.rol == user.rol

def test_get_user_by_id(test_db, test_user):
    """Test retrieving a user by ID."""
    # Fetch the user by ID
    fetched_user = User.by_id(test_user.id)
    assert fetched_user.id == test_user.id  # Ensure the fetched user matches the created one
    assert fetched_user.naam == test_user.naam
    assert fetched_user.rol == test_user.rol

def test_get_user_by_name(test_db, test_user):
    """Test retrieving a user by name."""
    # Fetch the user by name
    fetched_user = User.by_name(test_user.naam)
    assert fetched_user.naam == test_user.naam
    assert fetched_user.rol == test_user.rol

def test_all_users(test_db, test_user):
    """Test retrieving all users."""
    # Create additional users with unique names
    user2_name = f"UserTwo_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"
    user2 = User(naam=user2_name, rol="user")
    user2.create()

    user3_name = f"UserThree_{''.join(random.choices(string.ascii_letters + string.digits, k=8))}"
    user3 = User(naam=user3_name, rol="admin")
    user3.create()

    # Retrieve all users
    users = User.all()
    assert len(users) >= 3  # Ensure there are at least 3 users in the database
    assert any(u.id == test_user.id for u in users)
    assert any(u.id == user2.id for u in users)
    assert any(u.id == user3.id for u in users)

def test_get_non_existent_user_by_id(test_db):
    """Test retrieving a non-existent user by ID."""
    # Try to fetch a user with an invalid ID
    fetched_user = User.by_id(999999)  # Assuming this ID does not exist
    assert fetched_user is None  # Ensure that None is returned when the user is not found

def test_get_non_existent_user_by_name(test_db):
    """Test retrieving a non-existent user by name."""
    # Try to fetch a user with a non-existent name
    fetched_user = User.by_name("NonexistentUserName")
    assert fetched_user is None  # Ensure that None is returned when the user is not found
