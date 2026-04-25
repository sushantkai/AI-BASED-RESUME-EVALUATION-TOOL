from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import os

from jose import JWTError, jwt

from app.core.config import settings

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Format: pbkdf2_sha256$iterations$salt_b64$hash_b64
        scheme, iterations, salt_b64, hash_b64 = hashed_password.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64.encode("utf-8"))
        expected = base64.b64decode(hash_b64.encode("utf-8"))
        derived = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, int(iterations))
        return hmac.compare_digest(derived, expected)
    except Exception:
        return False


def hash_password(password: str) -> str:
    iterations = 100_000
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    salt_b64 = base64.b64encode(salt).decode("utf-8")
    hash_b64 = base64.b64encode(digest).decode("utf-8")
    return f"pbkdf2_sha256${iterations}${salt_b64}${hash_b64}"


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload.get("sub")
    except JWTError:
        return None
