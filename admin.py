from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from db.models.user import User
from core.security import verify_password
from fastapi import Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

def setup_admin():
    admin_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @admin_app.post("/login")
    async def login(request: Request):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        user = await User.get_or_none(username=username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"user": user, "token": "your_jwt_token_here"}  # Implement proper JWT token generation

    return admin_app