from typing import Any, AsyncContextManager, Callable, Mapping

from dishka import AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI

from backend.src.controllers.routes import router
from backend.src.infrastructure.middlewares import SessionMiddleware
from backend.src.infrastructure.repositories.sessions import (
    GuestSessionBackend,
    RedisSessionBackend,
)


async def create_fastapi_app(
    container: AsyncContainer, 
    lifespan: Callable[
        [FastAPI], AsyncContextManager[None]] | Callable[[FastAPI],
        AsyncContextManager[Mapping[str, Any]]
    ] | None
) -> FastAPI:
    fastapi_app = FastAPI(lifespan=lifespan)
    async with container() as opened:
        redis_backend = await opened.get(RedisSessionBackend)
        guest_backend = await opened.get(GuestSessionBackend)
    fastapi_app.include_router(router)
    fastapi_app.add_middleware(
        SessionMiddleware,
        redis_manager=redis_backend,
        guest_manager=guest_backend
    )
    fastapi_integration.setup_dishka(container=container, app=fastapi_app)
    return fastapi_app