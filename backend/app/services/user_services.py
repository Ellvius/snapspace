from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.users import User
from app.schemas.user_schema import UserCreate, UserOut


def create_user(user_data: UserCreate, db: Session) -> UserOut:
    user = User(**user_data.model_dump())
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return UserOut.model_validate(user)
    except IntegrityError:
        db.rollback()
        raise ValueError("Username or email already exists")


def get_user_by_username(username: str, db: Session) -> UserOut | None:
    result = db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return UserOut.model_validate(user) if user else None


def get_all_users(db: Session) -> list[UserOut]:
    result = db.execute(select(User))
    users = result.scalars().all()
    return [UserOut.model_validate(u) for u in users]
