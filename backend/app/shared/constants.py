# TODO: Define system constants
# - Validation rules
# - Error messages
# - Configuration values
# - Business rules

# User validation constants
MIN_ALIAS_LENGTH = 3
MAX_ALIAS_LENGTH = 50
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 128

# Error messages
ALIAS_REQUIRED_MSG = "Alias is required"
PASSWORD_REQUIRED_MSG = "Password is required"
PASSWORDS_MUST_MATCH_MSG = "Passwords must match"

# HTTP status codes
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_INTERNAL_ERROR = 500 