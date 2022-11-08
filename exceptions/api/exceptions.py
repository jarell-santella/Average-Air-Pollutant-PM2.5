class APIRequestQuotaError(Exception):

    def __init__(self, message = ""):
        super().__init__(message)

class APIInvalidKeyError(Exception):

    def __init__(self, message = ""):
        super().__init__(message)