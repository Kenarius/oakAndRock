import enum


class DomainErrorCodeEnum(enum.StrEnum):
    EMAIL_ALREADY_EXISTS = "email_already_exists"
    BIO_ID_ALREADY_EXISTS = "bio_id_already_exists"
    TAGNAME_ALREADY_EXISTS = "tag_already_exists"
    EMAIL_NOT_PROVIDED = "email_not_provided"
    INVALID_TOKEN = "invalid_token"
    TOKEN_EXPIRED = "expired_token"
    TOKEN_INVALID_OR_EXPIRED = "token_invalid_or_expired"
    WRONG_PASSWORD_PROVIDED = "wrong_password_provided"
    EMAIL_VERIFICATION_TOKEN_EXPIRED = "verification_token_expired"
    AUTHORIZATION_FAILED = "authorization_failed"
    PROVIDER_IS_NOT_REPRESENTED = "provider_not_represented"
    INCORRECT_RIGHT_ASSIGNMENT = "incorrect_rights_assignment"


class AuthorizationErrorCodeEnum(enum.StrEnum):
    USER_NOT_VERIFIED = "user_not_verified"


class DBErrorCodeEnum(enum.StrEnum):
    INVALID_CREDENTIALS = "invalid_credentials"
    USER_NOT_FOUND = "user_not_found"
    USER_DOES_NOT_EXISTS = "user_does_not_exists"
    OBJECT_NOT_FOUND = "object_not_found"
    GEO_HAS_NO_ATTRIBUTE = "geo_has_no_attribute"
    DB_FIELD_NOT_FOUND = "database_field_not_found"
