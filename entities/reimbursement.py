from abc import ABC


class Reimbursement(ABC):
    def __init__(self, r_id: int, reason: str, comment: str, amount: int, status: str, submitter_id: int, resolver_id: int,
                 submit_date: int,
                 resolve_date: int):
        self.r_id = r_id
        self.resolve_date = resolve_date
        self.submit_date = submit_date
        self.resolver_id = resolver_id
        self.submitter_id = submitter_id
        self.status = status
        self.amount = amount
        self.reason = reason
        self.comment = comment


    def __str__(self):
        return f"{self.r_id}, Reason: {self.reason}, Amt: {self.amount}, Status: {self.status}, By: {self.submitter_id} "

    def as_json_dict(self):
        return {
            "rId": self.r_id,
            "reason": self.reason,
            "comment": self.comment,
            "amount": self.amount,
            "status": self.status,
            "submitterId": self.submitter_id,
            "resolverId": self.resolver_id,
            "submitDate": self.submit_date,
            "resolveDate": self.resolve_date
        }
