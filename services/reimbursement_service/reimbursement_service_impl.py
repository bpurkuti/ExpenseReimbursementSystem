from typing import List

from daos.reimbursement_dao import ReimbursementDao
from entities.reimbursement import Reimbursement
from services.reimbursement_service.reimbursement_service import ReimbursementService


class ReimbursementServiceImpl(ReimbursementService):
    def __init__(self, r_dao: ReimbursementDao):
        self.r_dao = r_dao

    def create_reimbursement(self, reimbursement: Reimbursement) -> Reimbursement:
        return self.r_dao.create_reimbursement(reimbursement)

    def get_reimbursement(self, r_id: int, submitter_id: int) -> Reimbursement:
        return self.r_dao.get_reimbursement(r_id, submitter_id)

    def get_all_reimbursement(self) -> List[Reimbursement]:
        return self.r_dao.get_all_reimbursement()

    def get_all_reimbursement_by_employee(self, submitter_id: int) -> List[Reimbursement]:
        return self.r_dao.get_all_reimbursement_by_employee(submitter_id)

    def update_reimbursement(self, r_id: int, reimbursement: Reimbursement) -> Reimbursement:
        return self.r_dao.update_reimbursement(r_id, reimbursement)

    def delete_reimbursement(self, r_id: int) -> bool:
        return self.r_dao.delete_reimbursement(r_id)