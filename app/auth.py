from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from .config import get_settings
from .database import execute, fetch_one
from .models import User


password_hash = PasswordHash.recommended()

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed: str
) -> bool:
    return password_hash.verify(
        password,
        hashed
    )


def create_user(
    email: str,
    full_name: str,
    password: str
) -> User:

    row_id = execute(
        """
        INSERT INTO users
        (email, full_name, password_hash)
        VALUES (?, ?, ?)
        """,
        (
            email,
            full_name.strip(),
            hash_password(password)
        )
    )

    row = fetch_one(
        "SELECT * FROM users WHERE id = ?",
        (row_id,)
    )

    return row_to_user(row)


def get_user_by_email(email: str):

    row = fetch_one(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email.lower(),)
    )

    if not row:
        return None

    return row_to_user(row)


def get_user_by_id(user_id: int):

    row = fetch_one(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    if not row:
        return None

    return row_to_user(row)


def row_to_user(row) -> User:

    return User(
        id=row["id"],
        email=row["email"],
        full_name=row["full_name"],
        password_hash=row["password_hash"],
        created_at=row["created_at"],
    )


def create_access_token(
    user_id: int,
    expires_minutes: int = 60 * 24
) -> str:

    settings = get_settings()

    now = datetime.now(
        timezone.utc
    )

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(
            minutes=expires_minutes
        ),
    }

    return jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=ALGORITHM
    )


def decode_access_token(
    token: str
) -> int:

    settings = get_settings()

    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[ALGORITHM]
    )

    return int(payload["sub"])