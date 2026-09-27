from fastapi import (
    APIRouter,
    Depends
)

from ..dependencies import current_user
from ..database import fetch_all
from ..models import User


router = APIRouter(
    prefix="/api",
    tags=["session"]
)


@router.get(
    "/session-info"
)
async def session_info(
    user: User =
        Depends(current_user)
):

    return {

        "logged_in":
            True,

        "user_id":
            user.id,

        "email":
            user.email,

        "full_name":
            user.full_name
    }


@router.get(
    "/session-data"
)
async def session_data(
    user: User =
        Depends(current_user)
):

    rows = fetch_all(

        """
        SELECT
            planner_type,
            COUNT(*) AS count
        FROM recommendation_history
        WHERE user_id = ?
        GROUP BY planner_type
        """,

        (user.id,)
    )

    return {

        "user_id":
            user.id,

        "recommendation_counts": {

            row["planner_type"]:
                row["count"]

            for row in rows
        }
    }


@router.get(
    "/history"
)
async def history_api(
    user: User =
        Depends(current_user)
):

    rows = fetch_all(

        """
        SELECT
            id,
            planner_type,
            input_json,
            result_json,
            created_at
        FROM recommendation_history
        WHERE user_id = ?
        ORDER BY id DESC
        """,

        (user.id,)
    )

    return [
        dict(row)
        for row in rows
    ]