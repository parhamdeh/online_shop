from online_shop.core.exceptions import ApplicationError


class SMSGatewayException(ApplicationError):
    """
    Base exception for SMS Gateway.
    """

    def __init__(self, message="SMS gateway error.", extra=None):
        super().__init__(message=message, extra=extra)