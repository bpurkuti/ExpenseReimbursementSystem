from abc import ABC


class Employee(ABC):
    def __init__(self, e_id, first, last, username, password, is_manager):
        self.e_id = e_id
        self.first = first
        self.last = last
        self.username = username
        self.password = password
        self.is_manager = is_manager

    def __str__(self):
        return f"id={self.e_id}, Name ={self.first} {self.last}, Username: {self.username}, Manager: {self.is_manager}"

    def as_json_dict(self):
        return {
            "eId": self.e_id,
            "first": self.first,
            "last": self.last,
            "username": self.username,
            "isManager": self.is_manager,
        }
