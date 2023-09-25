from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config.settings import settings
from .crud.user import UserCRUD
from .schemas.token import TokenData
from .schemas.user import UserDB

# used to hash and verify passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2 bearer authentication method
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# function to verify if a received password matches the hashed password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# function to hash a password coming from the user
def get_password_hash(password):
    return pwd_context.hash(password)


# function to generate a new access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    # set expiration time for the token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode.update({"exp": expire})
    # Encode and generate new Token
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


async def get_user(username: str) -> UserDB:
    """
    Find user from db by 'username' and then return the user
    """
    return await UserCRUD.get_by_username(username)


async def authenticate_user(username: str, password: str) -> UserDB | bool:
    """
    Check if user exist in DB and then verify the password
    """
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserDB:
    """
    Get the UserDB authenticated by Token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode and get the payload Token
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        # Get the username and role from the payload
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        # Get TokenData
        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception
    # UserDB
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserDB, Depends(get_current_user)]
):
    """
    Get current UserDB that is available to get access
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
