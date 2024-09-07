from sqlalchemy.orm import Session
from app.databases.postgresdb.models import User
import app.databases.postgresdb.schemas as schemas
from sqlalchemy.exc import IntegrityError
from app.databases.postgresdb.authentication import get_password_hash


class DuplicateError(Exception):
    pass


def add_user(db: Session, user: schemas.UserSignUp, provider: str = None):
    if not provider and not user.password:
        raise ValueError("A password should be provided for non SSO registers")
    elif provider and user.password:
        raise ValueError("A password should not be provided for SSO registers")
    
    if user.password:
        password = get_password_hash(user.password)
    else:
        password = None

    user = User(
        username=user.username,
        password=password,
        fullname=user.fullname,
        provider=provider,
        picture=user.picture
    )
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise DuplicateError(
            f"Username {user.username} is already attached to a registered user for the provider '{provider}'.")
    return user


def get_user(db: Session, username: str, provider: str):
    user = db.query(User).filter(User.username == username).filter(User.provider == provider).first()
    return user

