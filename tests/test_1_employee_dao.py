import pytest
from daos.employee_dao import EmployeeDao
from daos.employee_dao_postgres import EmployeeDaoPostgres
from entities.employee import Employee
from exceptions.user_already_exists_error import UserAlreadyExistsError
from exceptions.user_doesnt_exist_error import UserDoesntExistError

e_dao: EmployeeDao = EmployeeDaoPostgres()


# def __init__(self, e_id, first, last, username, password, is_manager):
def test_create_employee1():
    user = Employee(0, "Bishwo", "Purkuti", "bpur", "password", False)
    res = e_dao.create_employee(user)
    assert user.username == res.username


def test_create_employee2():
    with pytest.raises(UserAlreadyExistsError):
        user = Employee(0, "Bishwo", "Purkuti", "bpur", "password", False)
        res = e_dao.create_employee(user)

def test_get_employee_by_id1():
    user = Employee(0, "Bishwo", "Purkuti", "EI1", "password", False)
    res = e_dao.create_employee(user)
    user = e_dao.get_employee_by_id(res.e_id)
    assert user.username == "EI1"

def test_get_employee_by_id2():
    with pytest.raises(UserDoesntExistError):
        user = e_dao.get_employee_by_id(0)

def test_get_employee_by_username1():
    user = Employee(0, "Bishwo", "Purkuti", "EU1", "password", False)
    res = e_dao.create_employee(user)
    user = e_dao.get_employee_by_username("EU1")
    assert user.e_id == res.e_id

def test_get_employee_by_username2():
    with pytest.raises(UserDoesntExistError):
        user = e_dao.get_employee_by_username("TestUserNameDoesntExist")

def test_get_all_employees():
    user1 = Employee(0, "Test1F", "Test1L", "test1", "test1", False)
    user2 = Employee(0, "Test2F", "Test2L", "test2", "test2", True)
    user3 = Employee(0, "Test3F", "Test3L", "test3", "test3", False)
    user4 = Employee(0, "Test4F", "Test4L", "test4", "test4", True)
    e_dao.create_employee(user1)
    e_dao.create_employee(user2)
    e_dao.create_employee(user3)
    e_dao.create_employee(user4)
    user_list = e_dao.get_all_employees()
    assert len(user_list) >= 5

def test_login1():
    user1 = Employee(0, "log", "In", "login", "pass", False)
    e_dao.create_employee(user1)
    result = e_dao.login(user1.username, user1.password)
    assert result

def test_login2():
    result = e_dao.login("UserdoesntExist", "PasswordDontExist")
    assert not result


