import json
from dataclasses import asdict
from typing import Optional
from uuid import UUID, uuid4

from fastapi import Request, Response
from redis.asyncio import Redis

from backend.src.application.interfaces import IGuestSessionBackend, ISessionBackend
from backend.src.domain.entities import SessionData
from backend.src.infrastructure.repositories.cookies import CookieRepo


class RedisSessionBackend(ISessionBackend[UUID, SessionData]):
    """Manages session storage in Redis."""

    def __init__(
        self,
        redis: Redis
    ) -> None:
        self._redis = redis

    async def create(
        self,
        session_id: UUID,
        data: SessionData
    ) -> None:
        """Creates a new session in Redis."""
        await self._redis.set(
            name=session_id.hex, 
            value=json.dumps(asdict(data)), 
            ex=3600
        )

    async def read(self, session_id: UUID) -> Optional[SessionData]:
        """Retrieves session data from Redis."""
        session_data = await self._redis.get(session_id.hex)
        return SessionData(
            **json.loads(session_data)
        ) if session_data else None

    async def update(self, session_id: UUID, data: SessionData) -> None:
        """Updates session data in Redis."""
        await self._redis.set(
            name=session_id.hex, 
            value=json.dumps(asdict(data)), 
            ex=3600
        )

    async def delete(self, session_id: UUID) -> None:
        """Deletes a session from Redis."""
        await self._redis.delete(session_id.hex)


class GuestSessionBackend(IGuestSessionBackend[UUID, dict]):
    """Handles guest session management using CookieManager."""

    def __init__(self, cookie_manager: CookieRepo):
        self._cookie_manager = cookie_manager

    def create_guest_session(self, response: Response) -> UUID:
        """Creates a new guest session."""
        session_id = uuid4()
        self._cookie_manager.set_cookie(
            response=response, 
            key=self._cookie_manager._GUEST_COOKIE, 
            value=str(session_id)
        )
        return session_id

    def get_guest_session(self, request: Request) -> Optional[UUID]:
        """Retrieves the current guest session."""
        session_id = self._cookie_manager.get_cookie(
            request=request, 
            key=self._cookie_manager._GUEST_COOKIE
        )
        return UUID(session_id) if session_id else None

    def delete_guest_session(self, response: Response) -> None:
        """Deletes the guest session."""
        self._cookie_manager.delete_cookie(
            response=response, 
            key=self._cookie_manager._GUEST_COOKIE
        )
        self._cookie_manager.delete_cookie(
            response=response, 
            key=self._cookie_manager._DATA_COOKIE
        )

    def update_guest_data(
            self, 
            request: Request,
            response: Response, 
            new_data: dict
        ) -> None:
        """Updates guest data while preserving existing information."""
        raw_data = self._cookie_manager.get_cookie(
            request=request, 
            key=self._cookie_manager._DATA_COOKIE
        )
        current_data = json.loads(
            raw_data
        ) if raw_data else {}
        current_data.update(new_data)
        self._cookie_manager.set_cookie(
            response=response, 
            key=self._cookie_manager._DATA_COOKIE, 
            value=json.dumps(current_data)
        )