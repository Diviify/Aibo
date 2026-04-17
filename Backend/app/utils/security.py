from passlib.context import CryptContext

# bcrypt_sha256 keeps bcrypt as the underlying algorithm while avoiding
# bcrypt's direct input-length edge cases.
password_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)
