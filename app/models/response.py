from pydantic import BaseModel


class ResponseMess(BaseModel):
    code: int
    message: str
