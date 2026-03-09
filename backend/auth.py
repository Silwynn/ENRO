from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "VERY_SUPER_SECRET_KEY_CHANGE_THIS"
ALGORITHM = "HS256"

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=8)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)