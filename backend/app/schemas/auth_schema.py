from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=3, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
