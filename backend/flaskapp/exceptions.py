from werkzeug.exceptions import HTTPException
from flaskapp.config import Config


class ServerError(HTTPException):
    pass


class InternalServerError(ServerError):
    def __init__(self, detail="An unexpected error occurred"):
        self.code = 500
        super().__init__(description=detail)


class ValidationError(HTTPException):
    pass


class RequestJsonError(ValidationError):
    def __init__(self):
        self.code = 400
        super().__init__(description="Bad request")


class UsernameError(ValidationError):
    def __init__(self):
        self.code = 400
        super().__init__(
            description=f"Username must be between {Config.MIN_NAME_LENGTH} and {Config.MAX_NAME_LENGTH} characters"
        )


class UserError(HTTPException):
    pass


class UserNotFoundError(UserError):
    def __init__(self):
        self.code = 404
        super().__init__(description="User not found")


class NoteError(HTTPException):
    pass


class NoteNotFound(NoteError):
    def __init__(self):
        self.code = 404
        super().__init__(description="Note not found")


class NotePinMismatchError(NoteError):
    def __init__(self):
        self.code = 403
        super().__init__(description="Invalid pin")


class NotePinRequiredError(NoteError):
    def __init__(self):
        self.code = 401
        super().__init__(description="Pin required")
