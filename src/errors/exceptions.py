class BaseServiceError(Exception):
    """Base exception for all service related errors."""
    def __init__(self, message, service_name):
        super().__init__(message)
        self.service_name = service_name

class TransientServiceError(BaseServiceError):
    """
    Errors that are temporary and usually resolved by retrying.
    Examples: 503 Service Unavailable, Network Timeouts, 429 Too Many Requests.
    """
    pass

class PermanentServiceError(BaseServiceError):
    """
    Errors that are permanent and should NOT be retried.
    Examples: 401 Unauthorized, 400 Bad Request, 403 Forbidden.
    """
    pass
