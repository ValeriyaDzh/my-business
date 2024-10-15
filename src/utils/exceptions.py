from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not found") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "Already exists"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
