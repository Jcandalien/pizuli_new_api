
from passlib.context import CryptContext

import os
from dotenv import load_dotenv

from db.models.user import User

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")



load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



