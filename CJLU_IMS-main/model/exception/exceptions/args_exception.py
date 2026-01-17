from model.exception.base_exceptions import ArgsException


# 参数相关
class ArgsEmptyException(ArgsException):
    """参数为空"""

    def __init__(self, message="参数为空", status_code=400):
        super().__init__(message, status_code)


class ArgsWrongException(ArgsException):
    """参数不合法"""

    def __init__(self, message="参数不合法", status_code=400):
        super().__init__(message, status_code)
