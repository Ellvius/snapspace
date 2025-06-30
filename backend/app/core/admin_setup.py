from app.core.db import SessionLocal
from app.config.settings import settings
from app.schemas.user_schema import UserRoles
from app.core.security import hash_password
from app.models.users import User

def create_admin():
    with SessionLocal() as db:
        if db.query(User).filter(User.role == UserRoles.ADMIN).first():
            return
        admin = User(
            username=settings.ADMIN_USERNAME,
            password=hash_password(settings.ADMIN_PASSWORD),
            role=UserRoles.ADMIN
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created.")
