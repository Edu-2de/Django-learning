from enum import StrEnum
from typing import Self

from django.core.exceptions import ValidationError


class BaseRuleError(StrEnum):
    message: str

    def __new__(cls, code: str, message: str) -> Self:
        member = str.__new__(cls, code)
        member._value_ = code
        member.message = message
        return member

    def to_validation_error(self) -> ValidationError:
        return ValidationError(self.message, code=self.value)
