from typing import List
from daos.reimbursement_dao import ReimbursementDao
from entities.reimbursement import Reimbursement
from exceptions.reimbursement_doesnt_exist import ReimbursementDoesntExistError
from exceptions.user_doesnt_exist_error import UserDoesntExistError
from utils.connection_util import connection


def check_employee(e_id: int) -> bool:
    sql = """select exists(select * from employee where e_id = %s)"""
    cursor = connection.cursor()
    cursor.execute(sql, [e_id])
    result = cursor.fetchone()[0]
    return result


class ReimbursementDaoPostgres(ReimbursementDao):

    def create_reimbursement(self, reimb: Reimbursement) -> Reimbursement:
        exists = check_employee(reimb.submitter_id)
        if exists:
            sql = """insert into reimbursement values(default, %s, %s, %s, %s, %s, %s ,current_timestamp at time zone 'PDT',%s) returning r_id;"""
            cursor = connection.cursor()
            cursor.execute(sql, [reimb.reason, reimb.comment, reimb.amount, reimb.status, reimb.submitter_id, 0,
                                 reimb.resolve_date])
            connection.commit()
            r_id = cursor.fetchone()[0]
            reimb.r_id = r_id
            return reimb
        else:
            raise UserDoesntExistError()

    def get_reimbursement(self, r_id: int, submitter_id: int) -> Reimbursement:
        exists = check_employee(submitter_id)
        if exists:
            sql = """select * from reimbursement where r_id = %s and submitter_id = %s;"""
            cursor = connection.cursor()
            cursor.execute(sql, [r_id, submitter_id])
            record = cursor.fetchone()
            if record is not None:
                reimbursement = Reimbursement(*record)
                return reimbursement
            else:
                raise ReimbursementDoesntExistError()
        else:
            raise UserDoesntExistError()

    def get_all_reimbursement(self) -> List[Reimbursement]:
        sql = """select * from reimbursement;"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        if records is not None:
            reimbursement = [Reimbursement(*record).as_json_dict() for record in records]
            return reimbursement
        else:
            raise ReimbursementDoesntExistError()

    def get_all_reimbursement_by_employee(self, submitter_id: int) -> List[Reimbursement]:
        exists = check_employee(submitter_id)
        if exists:
            sql = """select * from reimbursement where submitter_id = %s;"""
            cursor = connection.cursor()
            cursor.execute(sql, [submitter_id])
            records = cursor.fetchall()
            if records is not None:
                reimbursement = [Reimbursement(*record).as_json_dict() for record in records]
                return reimbursement
            else:
                raise ReimbursementDoesntExistError()
        else:
            raise UserDoesntExistError()

    def update_reimbursement(self, r_id: int, reimb: Reimbursement) -> Reimbursement:
        get_reimb = self.get_reimbursement(r_id, reimb.submitter_id)
        if get_reimb:
            sql = """update reimbursement set status = %s, comment = %s, resolver_id = %s, resolve_date = current_timestamp at time zone 'PDT' where r_id = %s and submitter_id = %s returning r_id, submitter_id;"""
            cursor = connection.cursor()
            cursor.execute(sql, [reimb.status, reimb.comment, reimb.resolver_id, r_id, reimb.submitter_id])
            connection.commit()
            reimbursement = self.get_reimbursement(r_id, reimb.submitter_id)
            return reimbursement
        else:
            raise ReimbursementDoesntExistError()

    def delete_reimbursement(self, r_id: int) -> bool:
        sql = """select exists(select * from reimbursement where r_id = %s);"""
        cursor = connection.cursor()
        cursor.execute(sql, [r_id])
        exists = cursor.fetchone()[0]
        if exists:
            sql = """delete from reimbursement where r_id = %s;"""
            cursor = connection.cursor()
            cursor.execute(sql, [r_id])
            connection.commit()
            return True
        else:
            raise ReimbursementDoesntExistError()
