import enum


class Roles(enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'


class DBErrorCodeEnum(enum.StrEnum):
    INVALID_CREDENTIALS = "invalid_credentials"
    USER_NOT_FOUND = "user_not_found"
    USER_DOES_NOT_EXISTS = "user_does_not_exists"
    OBJECT_NOT_FOUND = "object_not_found"
    GEO_HAS_NO_ATTRIBUTE = "geo_has_no_attribute"
    DB_FIELD_NOT_FOUND = "database_field_not_found"


class ServiceEnum(str, enum.Enum):
    OAK = "OAK"
