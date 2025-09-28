from werkzeug.exceptions import HTTPException


# ==============================
# Base Error Classes
# ==============================
class BaseAPIError(HTTPException):
    """Base class for all API errors."""

    code = 400
    description = "An unexpected error occurred"


class ServerError(BaseAPIError):
    """Base class for server-side errors (5xx)."""

    code = 500
    description = "Server error"


class ValidationError(BaseAPIError):
    """Base class for request validation errors (4xx)."""

    code = 400
    description = "Validation error"


class UserError(BaseAPIError):
    """Base class for user-related errors."""

    code = 400
    description = "User error"


class NoteError(BaseAPIError):
    """Base class for note-related errors."""

    code = 400
    description = "Note error"


# ==============================
# Server Errors (5xx)
# ==============================
class InternalServerError(ServerError):
    code = 500

    def __init__(self, detail="An unexpected error occurred"):
        super().__init__(description=detail)


# ==============================
# Validation Errors (4xx)
# ==============================
class RequestJsonError(ValidationError):
    code = 400
    description = "Bad request"


# ==============================
# User Errors (4xx)
# ==============================
class UserNotFoundError(UserError):
    code = 404
    description = "User not found!"


class UserEmailConflictError(UserError):
    code = 409
    description = {"emailStatus": "Email already taken"}


class UserUserNameConflictError(UserError):
    code = 409
    description = {"nameStatus": "Username already taken"}


class OtpError(UserError):
    code = 400
    description = "Timeout or invalid OTP"


class OtpRetryLimitError(UserError):
    code = 429
    description = "Please try again after 2 minutes"


class AuthenticationError(UserError):
    code = 401
    description = "Invalid credentials"


class ForbiddenAuthError(UserError):
    """Raised when an authenticated user tries to access a route which is only allowed for logged out user"""

    code = 403
    description = "Forbidden response!"


# ==============================
# Note Errors (4xx)
# ==============================
class NoteNotFound(NoteError):
    code = 404
    description = "Note not found"


class NotePinMismatchError(NoteError):
    code = 403
    description = "Invalid pin"


class NotePinRequiredError(NoteError):
    code = 401
    description = "Pin required"


class NoteDeleteForbiddenError(NoteError):
    code = 403
    description = "Delete not allowed!"


# ==============================
# JWT / Authentication Errors
# ==============================
class JWTError(BaseAPIError):
    """Base class for JWT-related errors."""

    code = 401
    description = "JWT validation error"


class TokenMissingError(JWTError):
    code = 401
    description = "Token is missing!"


class TokenExpiredError(JWTError):
    code = 401
    description = "Token has expired!"


class TokenInvalidError(JWTError):
    code = 401
    description = "Invalid token!"


class TokenPrefixError(JWTError):
    code = 401
    description = "Invalid token prefix!"
