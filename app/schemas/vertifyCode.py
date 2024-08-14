from pydantic import BaseModel, ValidationError, field_validator

class VerifyCodeModel(BaseModel):
    user_id: str
    code: str