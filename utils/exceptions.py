

class InsufficientStockError(Exception):
    pass


class BaseAppException(Exception):
    status_code = 400


class OrderNotFoundError(BaseAppException):
    pass


class PaymentAlreadyExistsError(BaseAppException):
    pass


class InvalidOrderStatusError(BaseAppException):
    pass


class InvalidPaymentStatusError(BaseAppException):
    pass

class PaymentNotFoundError(BaseAppException):
    pass


class PaymentInitializationError(BaseAppException):
    pass
