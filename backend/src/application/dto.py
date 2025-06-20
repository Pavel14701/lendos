from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LoginDto:
    username: str
    password: str


@dataclass(slots=True, frozen=True)
class UserDTO:
    id: int
    username: str


@dataclass(slots=True, frozen=True)
class UserSignupDTO:
    username: str
    password: str