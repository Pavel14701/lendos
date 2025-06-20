import secrets
from dataclasses import asdict

from backend.src.application.dto import (
    LoginDto,
    UserDTO,
    UserSignupDTO,
)
from backend.src.application.exceptions import (
    UserAlreadyExistsError,
)
from backend.src.application.interfaces import (
    IErrorHandler,
    ISecurity,
    ISession,
    IUser,
)
from backend.src.domain.entities import (
    PasswordDM,
    SignupPasswordDM,
    UserSignupDM,
)


class LoginInteractor:
    def __init__(
        self,
        user_repo: IUser,
        security_repo: ISecurity
    ) -> None:
        self._user_repo = user_repo
        self._security_repo = security_repo

    async def __call__(self, dto: LoginDto) -> int:
        user_dm = await self._user_repo.get_password(dto.username)
        password_dm = PasswordDM(
            salt=user_dm.salt,
            password=dto.password,
            hashed_password=user_dm.hashed_password
        )
        await self._security_repo.verify_password(password_dm)
        return user_dm.id


class GetUserInteractor:
    def __init__(
        self,
        user_repo: IUser
    ) -> None:
        self._user_repo = user_repo

    async def __call__(self, user_id: int) -> UserDTO:
        user = await self._user_repo.get_current_user(user_id)
        return UserDTO(**asdict(user))


class SignupInteractor:
    def __init__(
        self,
        session: ISession,
        security: ISecurity,
        user_repo: IUser,
        exc_handler: IErrorHandler 
    ) -> None:
        self._session = session
        self._security = security
        self._user_repo = user_repo
        self._exc_handler = exc_handler

    async def __call__(self, dto: UserSignupDTO) -> UserDTO:
        # sourcery skip: raise-from-previous-error
        try:
            password_input_model = SignupPasswordDM(
                salt=secrets.token_hex(8),
                password=dto.password
            )
            password_model = await self._security.hash_password(
                model=password_input_model
            )
            await self._user_repo.signup(UserSignupDM(
                username=dto.username,
                hashed_password=password_model.hashed_password,
                salt=password_model.salt
            ))
            await self._session.flush()
            user = await self._user_repo.get_user_by_username(dto.username)
            return UserDTO(**asdict(user))
        except Exception as e:
            raise self._exc_handler.handle_error(
                e, UserAlreadyExistsError
            )
