from pydantic import BaseModel


class SendOTPRequest(BaseModel):
    destination: str

class SendOTPResponse(BaseModel):
    session_code: str

class VerifyOTPRequest(BaseModel):
    code: str
    session_code: str

class ClaimOTPResponse(BaseModel):
    destination: str

class ErrorResponse(BaseModel):
    message: str