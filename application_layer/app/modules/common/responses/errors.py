from fastapi import HTTPException, status

class BadRequest(HTTPException):
    def __init__(self, detail="Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class Unauthorized(HTTPException):
    def __init__(self, detail="Not authenticated"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class Forbidden(HTTPException):
    def __init__(self, detail="The user doesn't have enough privileges"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class NotFound(HTTPException):
    def __init__(self, detail="Item not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ServerError(HTTPException):
    def __init__(self, detail="Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
