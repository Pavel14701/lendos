from dataclasses import asdict, dataclass
from typing import Self


@dataclass(slots=True)
class BaseDataClass:
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def replace(cls, instance: Self, **kwargs) -> Self:
        return cls(**{**instance.to_dict(), **kwargs})


@dataclass(slots=True, frozen=True)
class PasswordDM:
    salt: str
    password: str
    hashed_password: str


@dataclass(slots=True, frozen=True)
class UserDm:
    id: int
    username: str


@dataclass(slots=True, frozen=True)
class UserPasswordDM:
    id: int
    salt: str
    hashed_password: str


@dataclass(slots=True, frozen=True)
class SignupPasswordDM:
    salt: str
    password: str


@dataclass(slots=True, frozen=True)
class UserSignupDM:
    username: str
    hashed_password: str
    salt: str


# Off __slots__ because session type
# in FastAPI.Request is MutableMapping
@dataclass
class SessionData:
    user_id: int