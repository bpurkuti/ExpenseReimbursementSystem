from abc import ABC, abstractmethod
from typing import List

from entities.employee import Employee


class EmployeeDao(ABC):

    @abstractmethod
    def create_employee(self, employee: Employee) -> Employee:
        pass

    @abstractmethod
    def get_employee_by_id(self, e_id: int) -> Employee:
        pass

    @abstractmethod
    def get_employee_by_username(self, username: str) -> Employee:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        pass

    @abstractmethod
    def get_all_employees(self) -> List[Employee]:
        pass

    # @abstractmethod
    # def update_employee(self, e_id: int) -> Employee:
    #     pass
    #
    # @abstractmethod
    # def delete_employee(self, e_id: int) -> bool:
    #     pass
