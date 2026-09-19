from datetime import datetime, timedelta, timezone
import os

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# ============================================================
# CONFIGURATION
# ============================================================

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "SECRET_KEY must be set in the environment before starting the backend."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ============================================================
# OAUTH2 AUTHENTICATION
# ============================================================

# Swagger will use /auth/token to obtain the JWT.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


# ============================================================
# PASSWORD HASHING
# ============================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def _prepare_password(password: str) -> str:
    """
    bcrypt supports a maximum of 72 bytes.
    Safely limit the password to 72 UTF-8 bytes.
    """

    if not isinstance(password, str):
        raise ValueError("Password must be a string")

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]

    return password_bytes.decode(
        "utf-8",
        errors="ignore"
    )


def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    """

    safe_password = _prepare_password(password)

    return pwd_context.hash(safe_password)


def verify_password(
    password: str,
    password_hash: str
) -> bool:
    """
    Verify password against stored hash.
    """

    safe_password = _prepare_password(password)

    return pwd_context.verify(
        safe_password,
        password_hash
    )


# ============================================================
# JWT TOKEN CREATION
# ============================================================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.
    """

    to_encode = data.copy()

    if expires_delta:
        expire = (
            datetime.now(timezone.utc)
            + expires_delta
        )
    else:
        expire = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


# ============================================================
# JWT TOKEN VERIFICATION
# ============================================================

def verify_token(
    token: str
) -> dict | None:
    """
    Verify JWT token.

    Returns:
        JWT payload if valid
        None if invalid or expired
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        return None