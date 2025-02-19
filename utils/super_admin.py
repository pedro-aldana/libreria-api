from models.model_user import User, Role
from auth.auth import get_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

SUPERADMIN_EMAIL = os.getenv("SUPERADMIN_EMAIL")
SUPERADMIN_USERNAME = os.getenv("SUPERADMIN_USERNAME")
SUPERADMIN_PASSWORD = os.getenv("SUPERADMIN_PASSWORD")
SUPERADMIN_ROLE = os.getenv("SUPERADMIN_ROLE")

async def create_superadmin():
    # Verificar si el rol superadmin existe
    superadmin_role = await Role.get_or_none(name=SUPERADMIN_ROLE)
    if not superadmin_role:
        superadmin_role = await Role.create(name=SUPERADMIN_ROLE, description="Super Administrator")

    # Verificar si el superadmin ya existe
    existing_superadmin = await User.get_or_none(email=SUPERADMIN_EMAIL)
    if not existing_superadmin:
        hashed_password = get_password_hash(SUPERADMIN_PASSWORD)
        await User.create(
            email=SUPERADMIN_EMAIL,
            username=SUPERADMIN_USERNAME,
            password=hashed_password,
            role=superadmin_role
        )
        print(f"Superadmin created: {SUPERADMIN_EMAIL}")
