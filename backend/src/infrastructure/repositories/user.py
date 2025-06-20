from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.src.application.exceptions import UserNotFoundException
from backend.src.application.interfaces import IUser
from backend.src.domain.entities import (
    UserDm,
    UserPasswordDM,
    UserSignupDM
)
from backend.src.infrastructure.models import User


class UserRepo(IUser):
    """Repository for user-related database operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initializes the repository with an asynchronous database session."""
        self._session = session

    async def get_password(self, username: str) -> UserPasswordDM:
        """Retrieves the hashed password of a user by their username."""
        result = await self._session.execute(
            select(User).where(
                User.username == username
            )
        )
        if user := result.scalars().first():
            return user.to_domain(UserPasswordDM)
        raise UserNotFoundException()

    async def get_current_user(self, user_id: int) -> UserDm:
        """Fetches the current user's data by their user ID."""
        if user := await self._session.get(User, user_id):
            return user.to_domain(UserDm)
        raise UserNotFoundException()

    async def get_user_by_username(self, username: str) -> UserDm:
        """Fetches the current user's data by their user ID."""
        result = await self._session.execute(
            select(User).where(User.username == username)
        )
        if user := result.scalars().first():
            return user.to_domain(UserDm)
        raise UserNotFoundException()


    async def signup(self, signup_dm: UserSignupDM) -> None:
        """Registers a new user in the system."""
        model = User()
        model.hashed_password = signup_dm.hashed_password
        model.username = signup_dm.username
        model.salt = signup_dm.salt
        self._session.add(model)

