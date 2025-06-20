from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from backend.src.application.exceptions import InvalidPasswordException
from backend.src.application.interfaces import ISecurity
from backend.src.config import SecretConfig
from backend.src.domain.entities import PasswordDM, SignupPasswordDM


class SecurityRepo(ISecurity):
    """
    Handles password hashing 
    and verification using Argon2.
    """

    def __init__(
        self,
        password_hasher: PasswordHasher,
        app_config: SecretConfig 
    ) -> None:
        """
        Initializes the class with a password 
        hasher and application configuration.
        """
        self._password_hasher = password_hasher
        self._app_config = app_config

    async def verify_password(self, model: PasswordDM) -> None:
        """
        Verifies the provided password using 
        salt and pepper for added security.
        """
        try:
            salted_password = "{salt}{password}{pepper}".format(
                salt=model.salt,
                password=model.password,
                pepper=self._app_config.pepper
            )
            self._password_hasher.verify(
                hash=model.hashed_password, 
                password=salted_password
            )
        except (
            VerifyMismatchError, VerificationError, InvalidHashError
        ) as e:
            raise InvalidPasswordException() from e

    async def hash_password(self, model: SignupPasswordDM) -> PasswordDM:
        """
        Hashes the user's password using
        salt and pepper, returning a new 
        PasswordDM instance.
        """
        salted_password = "{salt}{password}{pepper}".format(
            salt=model.salt,
            password=model.password,
            pepper=self._app_config.pepper
        )
        hashed_password = self._password_hasher.hash(salted_password)
        return PasswordDM(model.salt, model.password, hashed_password)
