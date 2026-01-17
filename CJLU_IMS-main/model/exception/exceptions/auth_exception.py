# 用户相关异常
from model.exception.base_exceptions import AuthException


class UserNotExistException(AuthException):
    """用户不存在"""

    def __init__(self, message="用户不存在", status_code=404):
        super().__init__(message, status_code)


# 用户相关异常
class UserNotActiveException(AuthException):
    """用户已注销"""

    def __init__(self, message="用户已注销", status_code=404):
        super().__init__(message, status_code)


class RoleNotExistException(AuthException):
    """角色不存在"""

    def __init__(self, message="角色不存在", status_code=404):
        super().__init__(message, status_code)


class OldNewException(AuthException):
    """新旧密码相同"""

    def __init__(self, message="新旧密码相同", status_code=400):
        super().__init__(message, status_code)


class UserAlreadyExistsException(AuthException):
    """用户已存在"""

    def __init__(self, message="用户已存在", status_code=409):
        super().__init__(message, status_code)


class AuthenticationFailedException(AuthException):
    """认证失败"""

    def __init__(self, message="认证失败", status_code=401):
        super().__init__(message, status_code)


class TokenInvalidException(AuthException):
    """令牌无效"""

    def __init__(self, message="令牌无效", status_code=401):
        super().__init__(message, status_code)


class TokenExpiredException(AuthException):
    """令牌已过期"""

    def __init__(self, message="令牌已过期", status_code=401):
        super().__init__(message, status_code)


class PasswordErrorException(AuthException):
    """密码错误"""

    def __init__(self, message="密码错误", status_code=400):
        super().__init__(message, status_code)


class PermissionDeniedException(AuthException):
    """权限不足"""

    def __init__(self, message="权限不足", status_code=403):
        super().__init__(message, status_code)


class ResetPasswordWrongException(AuthException):
    """重置密码失败"""

    def __init__(self, message="重置密码失败", status_code=400):
        super().__init__(message, status_code)
