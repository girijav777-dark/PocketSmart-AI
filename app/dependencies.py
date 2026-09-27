from typing import Optional

from fastapi import (
    Cookie,
    Header,
    HTTPException,
    status
)

from .auth import (
    decode_access_token,
    get_user_by_id
)

from .models import User


def current_user(
    access_token: Optional[str] = Cookie(
        default=None
    ),
    authorization: Optional[str] = Header(
        default=None
    ),
) -> User:

    token = access_token

    if (
        not token
        and authorization
        and authorization.lower().startswith(
            "bearer "
        )
    ):
        token = authorization.split(
            " ",
            1
        )[1].strip()

    if not token:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required."
        )

    try:

        user_id = decode_access_token(
            token
        )

        user = get_user_by_id(
            user_id
        )

    except Exception:

        user = None

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    return user