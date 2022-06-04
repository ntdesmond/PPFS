from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


def verify_password(plain: str, hashed: str):
    return password_context.verify(plain, hashed)
