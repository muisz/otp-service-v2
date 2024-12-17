import environ
from fastapi import FastAPI, Depends, status
from fastapi.responses import Response
from typing import Annotated, Any

from app.dependency import get_database_connection
from app.schema import (
    ErrorResponse,
    SendOTPRequest,
    SendOTPResponse,
    VerifyOTPRequest,
    ClaimOTPResponse,
)
from app.repository import DatabaseOTPRepository
from app.service import OTPService
from app.exception import ClientErrorException

environ.Env()
environ.Env.read_env('.env')

app = FastAPI()

DbDep = Annotated[Any, Depends(get_database_connection)]

@app.get('/')
def root():
    return {'status': 'ok'}

@app.post('/send', status_code=status.HTTP_201_CREATED, response_model=SendOTPResponse)
def send(db: DbDep, otp: SendOTPRequest):
    repository = DatabaseOTPRepository(db)
    service = OTPService(repository)
    created_otp = service.create_otp(otp.destination)
    return SendOTPResponse(session_code=created_otp.session_code)

@app.post('/verify')
def verify(db: DbDep, otp: VerifyOTPRequest, response: Response):
    try:
        repository = DatabaseOTPRepository(db)
        service = OTPService(repository)
        service.get_otp(otp.code, otp.session_code)
        return

    except ClientErrorException as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponse(message=str(error))

@app.post('/claim')
def claim(db: DbDep, otp: VerifyOTPRequest, response: Response):
    try:
        repository = DatabaseOTPRepository(db)
        service = OTPService(repository)
        verified_otp = service.get_otp(otp.code, otp.session_code)
        service.delete(verified_otp)
        return ClaimOTPResponse(destination=verified_otp.destination)

    except ClientErrorException as error:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponse(message=str(error))
