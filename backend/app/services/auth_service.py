from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def login(self, username: str, password: str) -> dict:
        user = self.user_repository.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token(subject=user.username)
        return {"access_token": token, "role": user.role, "username": user.username}

    def ensure_seed_users(self) -> None:
        seed_users = [
            ("admin", "admin123", "Admin"),
            ("hr", "hr123", "HR"),
        ]
        for username, password, role in seed_users:
            existing = self.user_repository.get_by_username(username)
            if not existing:
                # Create new user
                self.user_repository.create_user(username=username, password_hash=hash_password(password), role=role)
                print(f"[SEED] Created user: {username} with role {role}")
            else:
                # Update existing user: ensure password hash is in correct format and role is correct
                if not (existing.password_hash and existing.password_hash.startswith("pbkdf2_sha256$")):
                    existing.password_hash = hash_password(password)
                    existing.role = role
                    self.user_repository.update_user(existing)
                    print(f"[SEED] Updated user: {username} with new password hash and role {role}")
