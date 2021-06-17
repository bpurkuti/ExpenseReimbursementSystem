from abc import ABC, abstractmethod
from typing import List

from entities.reimbursement import Reimbursement


class ReimbursementDao(ABC):

    @abstractmethod
    def create_reimbursement(self, reimbursement: Reimbursement) -> Reimbursement:
        pass

    @abstractmethod
    def get_reimbursement(self, r_id: int, submitter_id: int) -> Reimbursement:
        pass

    @abstractmethod
    def get_all_reimbursement(self) -> List[Reimbursement]:
        pass

    @abstractmethod
    def get_all_reimbursement_by_employee(self, submitter_id: int) -> List[Reimbursement]:
        pass

    @abstractmethod
    def update_reimbursement(self, r_id: int, reimbursement: Reimbursement) -> Reimbursement:
        pass

    @abstractmethod
    def delete_reimbursement(self, r_id: int) -> bool:
        pass
