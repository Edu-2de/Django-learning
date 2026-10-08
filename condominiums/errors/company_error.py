from setup.errors import BaseRuleError


class CompanyError(BaseRuleError):
    UNIQUE_EMAIL_FIELD = ("company.email_already_exists", "This email already exists")
