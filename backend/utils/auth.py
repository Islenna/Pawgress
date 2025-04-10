from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

# Password hashing context (uses bcrypt under the hood)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurable secrets
SECRET_KEY = "your_secret_here"  # Ideally store in an env variable!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Hash the user's password
def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

# Verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
