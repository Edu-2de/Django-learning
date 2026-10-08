import re

from ..errors.core_validator import CoreValidatorError


def validate_cep(value: str) -> None:
    pattern = re.compile(r"^\d{5}-?\d{3}$")

    if not pattern.match(value):
        raise CoreValidatorError.CEP_INVALID_CHECK_DIGITS.to_validation_error()
