from typing import List

from daos.employee_dao import EmployeeDao
from entities.employee import Employee
from exceptions.user_already_exists_error import UserAlreadyExistsError
from exceptions.user_doesnt_exist_error import UserDoesntExistError
from utils.connection_util import connection


class EmployeeDaoPostgres(EmployeeDao):
    def create_employee(self, employee: Employee) -> Employee:
        sql = """select exists(select * from employee where username = %s);"""
        cursor = connection.cursor()
        cursor.execute(sql, [employee.username])
        result = cursor.fetchone()[0]
        if not result:
            sql = """insert into employee values(default, %s, %s, %s, crypt(%s, gen_salt('bf')), %s)  returning e_id;"""
            cursor = connection.cursor()
            cursor.execute(sql,
                           [employee.first, employee.last, employee.username, employee.password, employee.is_manager])
            connection.commit()
            employee.e_id = cursor.fetchone()[0]
            return employee
        else:
            raise UserAlreadyExistsError()

    def get_employee_by_id(self, e_id: int) -> Employee:
        sql = """select * from employee where e_id = %s;"""
        cursor = connection.cursor()
        cursor.execute(sql, [e_id])
        record = cursor.fetchone()
        if record is not None:
            employee = Employee(*record)
            return employee
        else:
            raise UserDoesntExistError()

    def get_employee_by_username(self, username: str) -> Employee:
        sql = """select * from employee where username = %s;"""
        cursor = connection.cursor()
        cursor.execute(sql, [username])
        record = cursor.fetchone()
        if record is not None:
            employee = Employee(*record)
            return employee
        else:
            raise UserDoesntExistError()

    def login(self, username: str, password: str) -> bool:
        sql = """select exists(select * from employee where username = %s and password = crypt(%s, password));"""
        cursor = connection.cursor()
        cursor.execute(sql, [username, password])
        result = cursor.fetchone()[0]
        return result

    def get_all_employees(self) -> List[Employee]:
        sql = """select * from employee;"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        employee_list = [Employee(*record).as_json_dict() for record in records]
        if len(employee_list) > 0:
            return employee_list
        else:
            raise UserDoesntExistError()

    # Keeping them commented for now because IDK where I would use update and delete in this app
    # def update_employee(self, e_id: int) -> Employee:
    #     pass
    #
    # def delete_employee(self, e_id: int) -> bool:
    #     pass

