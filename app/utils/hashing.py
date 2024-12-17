from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_hashed_password(plain_password: str) -> str:
    """Generate hashed password"""
    return pwd_context.hash(plain_password)

def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the password valid"""
    return pwd_context.verify(plain_password, hashed_password)