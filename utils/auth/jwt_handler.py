# install PyJWT
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException
from config.settings import get_settings
import repositories.user_repository as user_repository
import schemas.user as user_schemas
 
JWT_SECRET_KEY = get_settings().secret_key
JWT_ALGORITHM = get_settings().algorithm
 
def create_access_token(*, data: dict, expires_delta: timedelta = None):
   to_encode = data.copy()
   if expires_delta:
      expire = datetime.utcnow() + expires_delta
   else:
      expire = datetime.utcnow() + timedelta(minutes=15)
   to_encode.update({"exp": expire})
   encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
   return encoded_jwt


def decode_access_token(db, token):
   credentials_exception = HTTPException(
      status_code=400,
      detail="Could not validate credentials",
      headers={"WWW-Authenticate": "Bearer"},
   )
   try:
      payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
      email: str = payload.get("sub")
      if email is None:
         raise credentials_exception
      token_data = user_schemas.User(email=email)
   except jwt.PyJWTError:
      raise credentials_exception
   user = user_repository.get_user_by_email(db, email=token_data.email)
   if user is None:
      raise credentials_exception
   return user