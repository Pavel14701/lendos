from typing import AsyncIterable
from uuid import uuid4

from argon2 import PasswordHasher
from dishka import AnyOf, Provider, Scope, from_context, provide
from faststream.rabbit import RabbitBroker
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.src.application import interfaces
from backend.src.application.interactors import (
    GetUserInteractor,
    LoginInteractor,
    SignupInteractor,
)
from backend.src.config import Config, SecretConfig
from backend.src.infrastructure.factories.postgres import new_session_maker
from backend.src.infrastructure.factories.redis import new_redis_client
from backend.src.infrastructure.repositories.cookies import CookieRepo
from backend.src.infrastructure.repositories.exc import ExceptionHandlersRepo
from backend.src.infrastructure.repositories.security import (
    SecurityRepo,
)
from backend.src.infrastructure.repositories.sessions import (
    GuestSessionBackend,
    RedisSessionBackend,
)
from backend.src.infrastructure.repositories.user import UserRepo


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)
    broker = from_context(provides=RabbitBroker, scope=Scope.APP)
    password_hasher = from_context(provides=PasswordHasher, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.UUIDGenerator:
        return uuid4

    @provide(scope=Scope.REQUEST)
    async def get_redis_conn(self, config: Config) -> AsyncIterable[Redis]:
        conn = await new_redis_client(config.redis)
        try:
            yield conn
        finally:
            await conn.aclose()

    @provide(scope=Scope.APP)
    def get_secret_config(self, config: Config) -> SecretConfig:
        return config.secret

    @provide(scope=Scope.APP)
    def get_session_maker(
        self, 
        config: Config
    ) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, 
        session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[
        AnyOf[AsyncSession, interfaces.ISession,]
    ]:
        async with session_maker() as session:
            yield session

    for name, (provider, interface) in {
        "cookie_repo": (
            CookieRepo, interfaces.ICookieBackend
        ),
        "error_handler_repo": (
            ExceptionHandlersRepo, interfaces.IErrorHandler
        ),
        "session_backend": (
            RedisSessionBackend, interfaces.ISessionBackend
        ),
        "guest_session_backend": (
            GuestSessionBackend, interfaces.IGuestSessionBackend
        ),
        "security_repo": (
            SecurityRepo, interfaces.ISecurity
        ),
        "user_repo": (
            UserRepo, interfaces.IUser
        ),
    }.items():
        vars()[name] = provide(provider, scope=Scope.REQUEST, provides=interface)

    for name, interactor in {
        "signup": SignupInteractor,
        "login": LoginInteractor,
        "get_user": GetUserInteractor,
    }.items():
        vars()[name] = provide(source=interactor, scope=Scope.REQUEST)
