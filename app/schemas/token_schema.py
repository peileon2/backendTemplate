from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str = Field(..., max_length=255)


class Token(BaseModel):
    access_token: str = Field(..., max_length=255)
    token_type: str = Field(default="bearer", max_length=255)


class TokenPayload(BaseModel):
    sub: int


class NewPassword(BaseModel):
    token: str = Field(..., max_length=255)
    new_password: str = Field(..., max_length=255)


class UserPublic(BaseModel):
    id: int


class UsersPublic(BaseModel):
    data: list[UserPublic]
    count: int
