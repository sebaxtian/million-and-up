from pydantic import BaseModel


class TokenSchema(BaseModel):
    """
    Token Schema representation
    access_token: str encoded jwt
    token_tyoe: str bearer authentication
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token Data to be encoded with jwt
    username: str unique user name
    role: str could be used as a scope
    """

    username: str
    role: str
