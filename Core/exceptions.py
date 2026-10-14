class UserError(Exception):
    """رسالة خطأ بتتعرض للمستخدم (زي odoo.exceptions.UserError)."""


class AccessError(Exception):
    """المستخدم ملوش صلاحية (زي odoo.exceptions.AccessError)."""