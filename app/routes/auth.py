from fastapi import (
    APIRouter,
    Form,
    Request,
    Response
)

from fastapi.responses import (
    JSONResponse,
    RedirectResponse
)

from pydantic import ValidationError

from ..auth import (
    create_access_token,
    create_user,
    get_user_by_email,
    verify_password
)

from ..schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse
)


router = APIRouter()


def _set_cookie(
    response: Response,
    token: str
):

    response.set_cookie(

        key="access_token",

        value=token,

        httponly=True,

        samesite="lax",

        secure=False,

        max_age=60 * 24 * 60
    )


@router.post("/register")
async def register_api(
    payload: RegisterRequest
):

    if get_user_by_email(
        payload.email
    ):

        return JSONResponse(
            {
                "detail":
                    "Email already registered."
            },
            status_code=409
        )

    try:

        user = create_user(
            payload.email,
            payload.full_name,
            payload.password
        )

    except Exception as exc:

        return JSONResponse(
            {
                "detail":
                    f"Registration failed: {exc}"
            },
            status_code=400
        )

    return {

        "id":
            user.id,

        "email":
            user.email,

        "full_name":
            user.full_name
    }


@router.post("/login")
async def login_api(
    payload: LoginRequest,
    response: Response
):

    user = get_user_by_email(
        payload.email.strip().lower()
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.password_hash
        )
    ):

        return JSONResponse(
            {
                "detail":
                    "Invalid email or password."
            },
            status_code=401
        )

    token = create_access_token(
        user.id
    )

    _set_cookie(
        response,
        token
    )

    return {

        "message":
            "Logged in",

        "user": {

            "id":
                user.id,

            "email":
                user.email,

            "full_name":
                user.full_name
        }
    }


@router.post(
    "/token",
    response_model=TokenResponse
)
async def token_api(
    payload: LoginRequest
):

    user = get_user_by_email(
        payload.email.strip().lower()
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user.password_hash
        )
    ):

        return JSONResponse(
            {
                "detail":
                    "Invalid email or password."
            },
            status_code=401
        )

    return TokenResponse(
        access_token=
            create_access_token(
                user.id
            )
    )


@router.post("/logout")
async def logout_api(
    response: Response
):

    response.delete_cookie(
        "access_token"
    )

    return {
        "message":
            "Logged out"
    }


@router.post("/register-form")
async def register_form(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):

    try:

        payload = RegisterRequest(
            full_name=full_name,
            email=email,
            password=password
        )

    except ValidationError:

        return RedirectResponse(
            "/register?error=Please+enter+valid+details",
            status_code=303
        )

    if get_user_by_email(
        payload.email
    ):

        return RedirectResponse(
            "/register?error=Email+already+registered",
            status_code=303
        )

    create_user(
        payload.email,
        payload.full_name,
        payload.password
    )

    return RedirectResponse(
        "/login?registered=1",
        status_code=303
    )


@router.post("/login-form")
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):

    user = get_user_by_email(
        email.strip().lower()
    )

    if (
        not user
        or not verify_password(
            password,
            user.password_hash
        )
    ):

        return RedirectResponse(
            "/login?error=Invalid+email+or+password",
            status_code=303
        )

    token = create_access_token(
        user.id
    )

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    _set_cookie(
        response,
        token
    )

    return response


@router.get("/logout")
async def logout_page():

    response = RedirectResponse(
        "/",
        status_code=303
    )

    response.delete_cookie(
        "access_token"
    )

    return response