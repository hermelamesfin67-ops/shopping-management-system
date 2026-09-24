

class InsufficientStockError(Exception):
    pass
class BaseAppException(Exception):
    status_code = 400