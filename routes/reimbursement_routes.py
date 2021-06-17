from flask import Flask, request, jsonify

from daos.reimbursement_dao_postgres import ReimbursementDaoPostgres
from entities.reimbursement import Reimbursement
from exceptions.reimbursement_doesnt_exist import ReimbursementDoesntExistError
from exceptions.user_doesnt_exist_error import UserDoesntExistError
from services.reimbursement_service.reimbursement_service import ReimbursementService
from services.reimbursement_service.reimbursement_service_impl import ReimbursementServiceImpl

r_service: ReimbursementService = ReimbursementServiceImpl(ReimbursementDaoPostgres())


def create_routes(app: Flask):
    # r_id: int, reason: str, amount: int, status: str, submitter_id: int, resolver_id: int, submit_date: int,
    # resolve_date: int

    @app.post('/employee/<e_id>/reimbursement')
    def create_reimbursement(e_id: str):
        try:
            body = request.json
            r = Reimbursement(0, body["reason"], "N/A", body["amount"], "Pending", body["submitterId"],
                              None, body["submitDate"], None)
            r.submitter_id = int(e_id)
            r = r_service.create_reimbursement(r)
            return f"Created a reimbursement with id: {r.r_id}", 201
        except UserDoesntExistError:
            return f"User doesn't exist", 404

    @app.get('/employee/<e_id>/reimbursement/<r_id>')
    def get_reimbursement(e_id: str, r_id: str):
        try:
            r = r_service.get_reimbursement(int(r_id), int(e_id))
            return jsonify(r.as_json_dict()), 200
        except UserDoesntExistError:
            return f"User doesn't exist", 404
        except ReimbursementDoesntExistError:
            return f"Reimbursement doesn't exist", 404

    @app.get('/employee/reimbursement')
    def get_all_reimbursement():
        try:
            r = r_service.get_all_reimbursement()
            return jsonify(r)
        except ReimbursementDoesntExistError:
            return f"Reimbursement doesn't exist", 404

    @app.get('/employee/<e_id>/reimbursement')
    def get_all_reimbursement_by_employee(e_id: str):
        try:
            r = r_service.get_all_reimbursement_by_employee(int(e_id))
            return jsonify(r)
        except UserDoesntExistError:
            return f"Employment doesn't exist", 404
        except ReimbursementDoesntExistError:
            return f"Reimbursement doesn't exist", 404

    @app.put('/employee/<e_id>/reimbursement/<r_id>')
    def update_reimbursement(e_id: str, r_id: str):
        try:
            body = request.json
            reimb = Reimbursement(0, body["reason"], body["comment"], body["amount"], body["status"], int(e_id),
                                  body["resolverId"], body["submitDate"], body["resolveDate"])
            r_service.update_reimbursement(int(r_id), reimb)
            return "Updated Successfully", 200
        except ReimbursementDoesntExistError:
            return f"Reimbursement doesn't exist", 404
        except UserDoesntExistError:
            return f"Employee doesn't exist", 404

    @app.delete('/employee/reimbursement/<r_id>')
    def delete_reimbursement(r_id: str):
        try:
            r_service.delete_reimbursement(int(r_id))
            return "Deleted successfully", 205
        except ReimbursementDoesntExistError:
            return "Reimbursement doesn't exist", 404
