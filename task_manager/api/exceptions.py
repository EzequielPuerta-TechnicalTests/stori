from werkzeug.exceptions import HTTPException


class ResourceNotFound(HTTPException):
    pass


class InvalidStateTransition(HTTPException):
    pass
