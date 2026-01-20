"""Authentication API routes."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.schemas import AuthResponse, ErrorResponse, LoginRequest, SignupRequest
from app.database import get_db
from app.exceptions import AuthenticationException, ResourceAlreadyExistsException
from app.models import UserRole
from app.services import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Email already registered"},
    },
)
def signup(request: SignupRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """Register a new user."""
    logger.info(f"Signup request received for email: {request.email}")

    auth_service = AuthService(db)

    try:
        user = auth_service.signup(request.email, request.password)
    except ResourceAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    logger.info(f"User registered successfully: {user['id']}")

    role_value = user["role"].value if isinstance(user["role"], UserRole) else user["role"]

    return AuthResponse(
        user_id=str(user["id"]),
        email=user["email"],
        role=role_value,
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
def login(request: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    """Login with email and password."""
    logger.info(f"Login request received for email: {request.email}")

    auth_service = AuthService(db)

    try:
        user = auth_service.login(request.email, request.password)
    except AuthenticationException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    logger.info(f"User logged in successfully: {user['id']}")

    role_value = user["role"].value if isinstance(user["role"], UserRole) else user["role"]

    return AuthResponse(
        user_id=str(user["id"]),
        email=user["email"],
        role=role_value,
    )


@router.get("/me", response_model=AuthResponse)
def get_current_user_info(user: dict = Depends(get_current_user)) -> AuthResponse:
    """Get current authenticated user info."""
    role_value = user["role"].value if isinstance(user["role"], UserRole) else user["role"]

    return AuthResponse(
        user_id=str(user["id"]),
        email=user["email"],
        role=role_value,
    )
