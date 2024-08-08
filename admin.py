import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from db.models.user import User
from core.security import verify_password
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup_admin():
    logger.info("Setting up admin app...")

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

    # Properly assign the login provider
    login_provider = UsernamePasswordProvider(
        login_logo_url="https://preview.tabler.io/static/logo.svg",
        admin_model=User,
    )
    admin_app.login_provider = login_provider

    async def login(request: Request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user = await User.get_or_none(username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return user

    admin_app.login_view = login

    return admin_app

def setup_admin2():
    logger = logging.getLogger(__name__)
    logger.info("Setting up admin app...")

    admin_app = FastAPI()

    @admin_app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception):
        logger.error(f"An error occurred: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred: {str(exc)}"},
        )

    @admin_app.get("/test")
    async def test_route():
        logger.info("Handling /test route")
        return {"message": "Admin is working!"}

    return admin_app
