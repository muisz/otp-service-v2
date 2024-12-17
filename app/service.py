import random
import string
import secrets
from typing import Union

from .repository import OTPRepository
from .model import OTP
from .exception import ClientErrorException

class OTPService:
    def __init__(self, repository: OTPRepository):
        self.repository = repository
    
    def create_otp(self, destination: str) -> OTP:
        otp = OTP(
            code=self.get_code(),
            session_code=self.get_session_code(),
            destination=destination
        )
        self.repository.create(otp)
        return otp

    def get_code(self):
        return ''.join(random.choice(string.digits) for _ in range(6))
    
    def get_session_code(self):
        return secrets.token_hex(5)

    def get_otp(self, code: str, session_code: str) -> OTP:
        otp = self.repository.get(code, session_code)
        if otp is None:
            raise ClientErrorException('Invalid OTP')
        return otp

    def delete(self, otp: OTP):
        self.repository.delete(otp.id)
