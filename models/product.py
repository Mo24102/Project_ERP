from Core.orm import Model
from Core.exceptions import UserError


class Product(Model):
    _name = "product.product"
    _defaults = {"active": True, "qty_available": 0}

    @classmethod
    def create(cls, vals):
        # Validation (زي @api.constrains في Odoo)
        if vals.get("price", 0) < 0:
            raise UserError("Price cannot be negative.")
        if not vals.get("name"):
            raise UserError("Product name is required.")
        return super().create(vals)


class Partner(Model):
    _name = "res.partner"
    _defaults = {"is_customer": True}