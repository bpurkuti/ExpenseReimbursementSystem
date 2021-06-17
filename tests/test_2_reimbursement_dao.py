import pytest

from daos.employee_dao import EmployeeDao
from daos.employee_dao_postgres import EmployeeDaoPostgres
from daos.reimbursement_dao import ReimbursementDao
from daos.reimbursement_dao_postgres import ReimbursementDaoPostgres
from entities.employee import Employee
from entities.reimbursement import Reimbursement
from exceptions.reimbursement_doesnt_exist import ReimbursementDoesntExistError
from exceptions.user_doesnt_exist_error import UserDoesntExistError

r_dao: ReimbursementDao = ReimbursementDaoPostgres()
e_dao: EmployeeDao = EmployeeDaoPostgres()

user1 = Employee(0, "rtest1", "Purkuti", "rtest1", "password", False)
user2 = Employee(0, "rtest2", "Purkuti", "rtest2", "password", False)

res1 = e_dao.create_employee(user1)
res2 = e_dao.create_employee(user2)
e_id1 = res1.e_id
e_id2 = res2.e_id


# (r_id: int, reason: str, amount: int, status: str, submitter_id: int, resolver_id: int, submit_date: int,
# resolve_date: int)
def test_create_reimbursement1():
    test1 = Reimbursement(0, "Food", None, 123, "Pending", e_id1, None, None, None)
    res = r_dao.create_reimbursement(test1)
    assert res.r_id != 0


def test_create_reimbursement2():
    with pytest.raises(UserDoesntExistError):
        test1 = Reimbursement(0, "Food", None, 123, "Pending", 0, None, 1623439247, None)
        r_dao.create_reimbursement(test1)


def test_create_reimbursement3():
    with pytest.raises(UserDoesntExistError):
        test1 = Reimbursement(0, "Food", None, 123, "Pending", 999, None, 1623439247, None)
        r_dao.create_reimbursement(test1)


def test_get_reimbursement1():
    res = r_dao.get_reimbursement(1, e_id1)
    assert res.r_id == 1


def test_get_reimbursement2():
    with pytest.raises(ReimbursementDoesntExistError):
        r_dao.get_reimbursement(0, e_id1)


def test_get_reimbursement3():
    with pytest.raises(UserDoesntExistError):
        r_dao.get_reimbursement(1, 0)


def test_get_all_reimbursement():
    test1 = Reimbursement(0, "Accident", None, 424, "Pending", e_id1, None, 1623439247, None)
    test2 = Reimbursement(0, "Hell", None, 666, "Pending", e_id1, None, 1623439247, None)
    test3 = Reimbursement(0, "Lodging", None, 100, "Pending", e_id1, None, 1623439247, None)
    r_dao.create_reimbursement(test1)
    r_dao.create_reimbursement(test2)
    r_dao.create_reimbursement(test3)
    res = r_dao.get_all_reimbursement()
    assert len(res) >= 4


def test_get_all_reimbursement_by_employee1():
    test1 = Reimbursement(0, "Phone Bill", None, 300, "Pending", e_id2, None, 1623439247, None)
    test2 = Reimbursement(0, "Dog ate Homework", None, 50, "Pending", e_id2, None, 1623439247, None)
    test3 = Reimbursement(0, "Broke", None, 20, "Pending", e_id2, None, 1623439247, None)
    r_dao.create_reimbursement(test1)
    r_dao.create_reimbursement(test2)
    r_dao.create_reimbursement(test3)
    res = r_dao.get_all_reimbursement_by_employee(e_id2)
    assert len(res) >= 3


def test_get_all_reimbursement_by_employee2():
    with pytest.raises(UserDoesntExistError):
        r_dao.get_all_reimbursement_by_employee(0)


def test_update_reimbursement1():
    test1 = Reimbursement(0, "Uber", None, 500, "Pending", e_id2, None, 1623439247, None)
    res = r_dao.create_reimbursement(test1)
    res.status = "Denied"
    res.resolver_id = 3
    res = r_dao.update_reimbursement(res.r_id, res)
    assert res.status == "Denied"


def test_update_reimbursement2():
    with pytest.raises(ReimbursementDoesntExistError):
        test1 = Reimbursement(0, "Uber", None, 500, "Pending", e_id2, None, 1623439247, None)
        test1.status = "Denied"
        test1.comment = "Pay with your own money"
        res = r_dao.update_reimbursement(0, test1)


def test_delete_reimbursement1():
    test1 = Reimbursement(0, "Gas", None, 300, "Pending", e_id1, None, 1623439247, None)
    res = r_dao.create_reimbursement(test1)
    result = r_dao.delete_reimbursement(res.r_id)
    assert result


def test_delete_reimbursement2():
    with pytest.raises(ReimbursementDoesntExistError):
        r_dao.delete_reimbursement(0)
