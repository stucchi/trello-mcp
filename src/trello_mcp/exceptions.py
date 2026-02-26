class TrelloError(Exception):
    def __init__(self, message: str, status_code: int = 0) -> None:
        super().__init__(message)
        self.status_code = status_code


class TrelloAuthError(TrelloError):
    pass


class TrelloNotFoundError(TrelloError):
    pass


class TrelloRateLimitError(TrelloError):
    pass
