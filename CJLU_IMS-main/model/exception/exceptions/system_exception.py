from model.exception.base_exceptions import SystemException


class PublicKeyNotFoundException(SystemException):

    def __init__(self, message="公钥不存在", status_code=500):
        super().__init__(message, status_code)


class StaticFileNotFoundException(SystemException):

    def __init__(self, message="静态文件未找到", status_code=500):
        super().__init__(message, status_code)
