import json

from fastapi import (
    APIRouter,
    Depends,
    Request
)

from fastapi.responses import (
    HTMLResponse,
    RedirectResponse
)

from fastapi.templating import (
    Jinja2Templates
)

from ..database import fetch_all
from ..dependencies import current_user


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


@router.get(
    "/",
    response_class=HTMLResponse
)
async def home(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "index.html"
    )


@router.get(
    "/register",
    response_class=HTMLResponse
)
async def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "register.html"
    )


@router.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request,
        "login.html"
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(
    request: Request,
    user=Depends(current_user)
):

    history = fetch_all(
        """
        SELECT
            id,
            planner_type,
            created_at
        FROM recommendation_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 8
        """,
        (user.id,)
    )

    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "user": user,
            "history": history
        }
    )


@router.get(
    "/history",
    response_class=HTMLResponse
)
async def history(
    request: Request,
    user=Depends(current_user)
):

    rows = fetch_all(
        """
        SELECT *
        FROM recommendation_history
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (user.id,)
    )

    records = []

    for row in rows:

        records.append(
            {
                "id": row["id"],
                "planner_type": row["planner_type"],
                "created_at": row["created_at"],
                "result": json.loads(
                    row["result_json"]
                )
            }
        )

    return templates.TemplateResponse(
        request,
        "history.html",
        {
            "user": user,
            "records": records
        }
    )


@router.get(
    "/planner/{planner_type}",
    response_class=HTMLResponse
)
async def planner_page(
    request: Request,
    planner_type: str,
    user=Depends(current_user)
):

    if planner_type not in {
        "home",
        "party",
        "jewelry"
    }:

        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request,
        "planner.html",
        {
            "user": user,
            "planner_type": planner_type
        }
    )