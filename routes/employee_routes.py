from flask import Flask, request, jsonify

from daos.employee_dao_postgres import EmployeeDaoPostgres
from entities.employee import Employee
from exceptions.user_already_exists_error import UserAlreadyExistsError
from exceptions.user_doesnt_exist_error import UserDoesntExistError
from services.employee_service.employee_service_impl import EmployeeServiceImpl

e_dao = EmployeeDaoPostgres()
e_service = EmployeeServiceImpl(e_dao)


def create_routes(app: Flask):
    @app.post('/employee')
    def create_employee():
        try:
            body = request.json
            employee = Employee(0, body["first"], body["last"], body["username"], body["password"], body["isManager"])
            e_service.create_employee(employee)
            return f"Created a employee with id: {employee.e_id}", 201
        except UserAlreadyExistsError:
            return f"Username is already taken", 404
        except TypeError:
            return f"Username is already taken", 404

    @app.get('/employee/id/<e_id>')
    def get_employee_by_id(e_id: str):
        try:
            employee = e_service.get_employee_by_id(int(e_id))
            return jsonify(employee.as_json_dict())
        except UserDoesntExistError:
            return f"Employee with id: {e_id} doesn't exist", 404

    @app.get('/employee/username/<username>')
    def get_employee_by_username(username: str):
        try:
            employee = e_service.get_employee_by_username(username)
            return jsonify(employee.as_json_dict())
        except UserDoesntExistError:
            return f"Employee with username: {username} doesn't exist", 404

    @app.get('/employee')
    def get_all_employee():
        try:
            employees = e_service.get_all_employees()
            return jsonify(employees), 200
        except UserDoesntExistError:
            return f"No Employees found", 404

    @app.post('/employee/login')
    def login():
        body = request.json
        result = e_service.login(body["username"], body["password"])
        if result:
            return f"Logged in {body['username']} successfully!", 200
        else:
            return f"Password is incorrect.", 403
