from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from db.models.user import User
from core.security import verify_password
from fastapi import Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException

def setup_admin():
    # Custom exception handler
    @admin_app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred: {str(exc)}"},
        )

    admin_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    login_provider = UsernamePasswordProvider(
        login_logo_url="https://preview.tabler.io/static/logo.svg",
        admin_model=User
    )

    async def login(request: Request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user = await User.get_or_none(username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    admin_app.login_provider = login_provider
    admin_app.login_view = login

    return admin_app