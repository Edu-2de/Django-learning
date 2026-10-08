from .base import BaseRuleError


class CoreValidatorError(BaseRuleError):
    CPF_INVALID_LENGTH = (
        "cpf.invalid_length",
        "CPF must have 11 digits, without punctuation.",
    )
    CPF_INVALID_CHECK_DIGITS = ("cpf.invalid_check_digits", "Invalid CPF.")
    CNPJ_INVALID_LENGTH = (
        "cnpj.invalid_length",
        "CNPJ must have 14 characters, without punctuation.",
    )
    CNPJ_INVALID_CHECK_DIGITS = ("cnpj.invalid_check_digits", "Invalid CNPJ.")
    CEP_INVALID_CHECK_DIGITS = ("cep.invalid_check_digis", "Invalid CEP")
    PERCENTAGE_OUT_OF_RANGE = (
        "percentage.out_of_range",
        "Percentage must be between 0 and 100.",
    )
