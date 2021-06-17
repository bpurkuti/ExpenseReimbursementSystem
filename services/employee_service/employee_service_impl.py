from typing import List

from daos.employee_dao import EmployeeDao
from daos.employee_dao_postgres import EmployeeDaoPostgres
from entities.employee import Employee
from exceptions.user_doesnt_exist_error import UserDoesntExistError
from services.employee_service.employee_service import EmployeeService


class EmployeeServiceImpl(EmployeeService):
    def __init__(self, e_dao: EmployeeDao):
        self.e_dao = e_dao

    def create_employee(self, employee: Employee) -> Employee:
        return self.e_dao.create_employee(employee)

    def get_employee_by_id(self, e_id: int) -> Employee:
        return self.e_dao.get_employee_by_id(e_id)

    def get_employee_by_username(self, username: str) -> Employee:
        return self.e_dao.get_employee_by_username(username)

    def get_all_employees(self) -> List[Employee]:
        return self.e_dao.get_all_employees()

    def login(self, username: str, password: str) -> bool:
        return self.e_dao.login(username, password)

