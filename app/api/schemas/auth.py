"""Pydantic schemas for authentication."""

from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupRequest(BaseModel):
    """Signup request schema."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v:
            raise ValueError("Password cannot be empty")
        return v


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Authentication response schema."""

    user_id: str
    email: str
    role: str


class ErrorResponse(BaseModel):
    """Error response schema."""

    error: str
    message: str
