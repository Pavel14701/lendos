from sqlalchemy.exc import IntegrityError

from backend.src.application.exceptions import DomainException
from backend.src.application.interfaces import IErrorHandler


class ExceptionHandlersRepo(IErrorHandler[DomainException]):
    """Repository for handling application exceptions."""

    def handle_error(
        self,
        error: Exception,
        _raise: type[DomainException]
    ) -> DomainException:
        return _raise() if isinstance(error, IntegrityError) else _raise(str(error))
