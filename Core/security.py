from functools import wraps
from Core.exceptions import AccessError

# المستخدمين والمجموعات (زي res.users و res.groups)
USERS = {
    "admin": {"groups": ["sales_manager", "sales_user"]},
    "ali": {"groups": ["sales_user"]},
}

class Env:
    user = "admin"          # المستخدم الحالي


def requires_group(group):
    """Decorator بيمنع تنفيذ الدالة لو المستخدم مش في المجموعة."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            groups = USERS[Env.user]["groups"]
            if group not in groups:
                raise AccessError(
                    f"User '{Env.user}' needs group '{group}'")
            return func(*args, **kwargs)
        return wrapper
    return decorator