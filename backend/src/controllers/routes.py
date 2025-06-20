from dataclasses import asdict
from typing import Any

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException, Request

from backend.src.application.dto import LoginDto, UserSignupDTO
from backend.src.application.exceptions import (
    InvalidPasswordException,
    UserAlreadyExistsError,
    UserNotFoundException,
)
from backend.src.application.interactors import (
    GetUserInteractor,
    LoginInteractor,
    SignupInteractor,
)
from backend.src.controllers.schemas import (
    OkxWebSocketConfigRequest,
    UserLoginRequest,
    UserSignupRequest,
)

router = APIRouter()


class UserRoutes:
    @router.post("/login/")
    @inject
    async def login(
        self, 
        request_body: UserLoginRequest,
        request: FromDishka[Request],
        interactor: FromDishka[LoginInteractor]
    ) -> dict[str, str]:
        dto = LoginDto(**request_body.model_dump())
        try:
            user_id = await interactor(dto)
        except UserNotFoundException as e:
            raise HTTPException(status_code=404, detail="User not found") from e
        except InvalidPasswordException as e:
            raise HTTPException(status_code=401, detail="Invalid password") from e
        request.session["user_id"] = user_id
        return {"message": "Logged in successfully"}

    @router.get("/logout/")
    @inject
    async def logout(
        self, 
        request: FromDishka[Request],
    ) -> dict[str, str]:
        request.session.clear()
        return {"message": "Logged out successfully"}

    @router.post("/signup")
    @inject
    async def create_user(
        self,
        request_body: UserSignupRequest,
        interactor: FromDishka[SignupInteractor]
    ) -> dict[str, int | str]:
        dto = UserSignupDTO(**request_body.model_dump())
        try:
            user = await interactor(dto)
        except UserAlreadyExistsError as e:
            raise HTTPException(
                status_code=409, detail="User with this username already exists."
            ) from e
        return {"id": user.id, "username": user.username}

    @router.get("/me/")
    @inject
    async def get_current_user(
        self, 
        request: FromDishka[Request],
        interactor: FromDishka[GetUserInteractor]
    ) -> dict[str, int | str]:
        user_id: int | None = request.session.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Not authenticated")
        try:
            user = await interactor(user_id)
        except UserNotFoundException as e:
            raise HTTPException(status_code=404, detail="User not found") from e
        return {"id": user.id, "username": user.username}