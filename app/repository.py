from typing import Union

from .model import OTP

class OTPRepository:
    def create(self, otp: OTP):
        raise NotImplementedError()
    
    def get(self, code: str, session_code: str) -> Union[OTP, None]:
        raise NotImplementedError()
    
    def delete(self, id: int):
        raise NotImplementedError()


class DatabaseOTPRepository(OTPRepository):
    def __init__(self, db):
        self.db = db
    
    def create(self, otp: OTP):
        with self.db.cursor() as cursor:
            cursor.execute(
                "insert into otps (code, session_code, destination) values (%s, %s, %s)",
                [otp.code, otp.session_code, otp.destination]
            )
            self.db.commit()
    
    def get(self, code: str, session_code: str) -> Union[OTP, None]:
        with self.db.cursor() as cursor:
            cursor.execute("select id, code, session_code, destination, created_at, updated_at from otps where code = %s and session_code = %s;", [code, session_code])
            result = cursor.fetchone()
            if result:
                return OTP(
                    id=result[0],
                    code=result[1],
                    session_code=result[2],
                    destination=result[3],
                    created_at=result[4],
                    updated_at=result[5],
                )
        return None
    
    def delete(self, id: int):
        with self.db.cursor() as cursor:
            cursor.execute("delete from otps where id = %s;", [id])
            self.db.commit()
