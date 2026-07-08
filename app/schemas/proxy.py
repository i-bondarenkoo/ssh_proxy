from pydantic import BaseModel


class ValidateDataIn(BaseModel):
    ip: str
    command: str
