class AppError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(f'{reason}')
        self.reason = reason


class NotFoundFileConfigError(AppError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason=reason)


class NotFoundKeyConfigError(AppError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason=reason)


class InvalidSelectorSeleniumError(AppError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason=reason)


class NoSuchElementError(AppError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason=reason)


class NotFoundRequestError(AppError):
    def __init__(self, reason: str) -> None:
        super().__init__(reason=reason)
