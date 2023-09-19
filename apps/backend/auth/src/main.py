from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .config.settings import settings
from .db.motor import Motor
from .routers import auth
from .schemas.token import TokenSchema
from .schemas.user import UserCreate
from .utils import authenticate_user, create_access_token, get_password_hash

app = FastAPI(version=settings.version, title=settings.name)

# Add created endpoints
app.include_router(auth.router)


@app.post("/token", response_model=TokenSchema)
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login to get Token using the OAuth2PasswordRequestForm built-in form FastAPI
    TODO: Update to use OAuth2 scopes instead of "role" Token payload attribute
    https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    # Create Token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.on_event("startup")
async def open_db_conn():
    """Initialize DB connection"""

    await Motor.connect()
    # Create admin user once
    result = await Motor.db.users.find_one({"username": "admin"})
    if not result:
        admin = UserCreate(
            email="admin@example.com",
            username=settings.admin_user,
            full_name="Admin User",
            hashed_password=get_password_hash(settings.admin_pwd),
        )
        result = await Motor.db.users.insert_one(admin.to_mongo())
        if not result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Admin User can not be created!",
            )


@app.on_event("shutdown")
async def close_db_conn():
    """Close DB connection"""

    await Motor.close()
