from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.users import User
from app.schemas.user_schema import UserCreate, UserOut, UserWithContainers


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


def get_user_by_username(username: str, db: Session) -> User | None:
    result = db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    return user

def get_user_by_id(user_id: str, db: Session) -> UserOut | None:
    user = db.query(User).filter(User.id == user_id).first()
    return UserOut.model_validate(user)


def get_all_users(db: Session) -> list[UserOut]:
    result = db.execute(select(User))
    users = result.scalars().all()
    return [UserOut.model_validate(u) for u in users]


def get_user_with_containers(user_id: int, db: Session) -> UserWithContainers | None:
    result = (
        db.query(User)
        .options(joinedload(User.containers))
        .filter(User.id == user_id)
        .first()
    )
    return UserWithContainers.model_validate(result)
    

def delete_user_by_id(user_id: int, db: Session) -> UserOut | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    try:
        db.delete(user)
        db.commit()
        return UserOut.model_validate(user)
    except Exception as e:
        raise ValueError("Error deleting user") from e