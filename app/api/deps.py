"""FastAPI dependencies for authentication and authorization."""

import logging

from fastapi import Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import AuthenticationException, AuthorizationException
from app.models import UserRole
from app.repositories import UserRepository
from app.security import decode_access_token

logger = logging.getLogger(__name__)

security = HTTPBasic()


def get_current_user(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    """Get current authenticated user from Basic Auth or JWT."""
    user = _authenticate_user(credentials, db)

    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            token_data = decode_access_token(token)
            if token_data.get("sub") != str(user["id"]):
                raise AuthorizationException("Token does not match user")
        except ValueError:
            pass

    return user


def _authenticate_user(
    credentials: HTTPBasicCredentials,
    db: Session,
) -> dict:
    """Authenticate user with Basic Auth credentials."""
    user_repository = UserRepository(db)
    user = user_repository.find_by_email(credentials.username)

    if user is None:
        raise AuthenticationException("Invalid email or password")

    from app.security import verify_password

    if not verify_password(credentials.password, user["password_hash"]):
        raise AuthenticationException("Invalid email or password")

    return user


def require_role(required_role: UserRole):
    """Factory for role-checking dependency."""

    def role_checker(user: dict = Depends(get_current_user)) -> dict:
        user_role = user["role"]
        if isinstance(user_role, UserRole):
            user_role = user_role.value

        role_hierarchy = [UserRole.USER, UserRole.ADMIN]
        user_role_level = role_hierarchy.index(
            UserRole.USER if user_role == "USER" else UserRole.ADMIN
        )
        required_role_level = role_hierarchy.index(required_role)

        if user_role_level < required_role_level:
            raise AuthorizationException(f"Role {required_role.name} required")
        return user

    return role_checker


def get_current_admin(user: dict = Depends(require_role(UserRole.ADMIN))) -> dict:
    """Require admin role."""
    return user
