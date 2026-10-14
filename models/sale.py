from Core.orm import Model
from Core.exceptions import UserError
from Core.security import requires_group
from models.product import Product


class SaleOrderLine(Model):
    _name = "sale.order.line"
    _defaults = {"qty": 1}

    @classmethod
    def create(cls, vals):
        product = Product.browse(vals["product_id"])
        # لو السعر مش متحدد ناخده من المنتج (زي onchange)
        vals.setdefault("price_unit", product["price"])
        vals["subtotal"] = vals["price_unit"] * vals.get("qty", 1)
        return super().create(vals)


class SaleOrder(Model):
    _name = "sale.order"
    _defaults = {"state": "draft", "discount": 0}

    @classmethod
    def compute_total(cls, order_id):
        """زي computed field: amount_total"""
        line_ids = SaleOrderLine.search([("order_id", "=", order_id)])
        return sum(SaleOrderLine.browse(l)["subtotal"] for l in line_ids)

    @classmethod
    @requires_group("sales_user")
    def action_confirm(cls, order_id):
        order = cls.browse(order_id)
        if order["state"] != "draft":
            raise UserError("Only draft orders can be confirmed.")
        if cls.compute_total(order_id) <= 0:
            raise UserError("Cannot confirm an empty order.")
        cls.write(order_id, {"state": "confirmed"})
        return True

    @classmethod
    @requires_group("sales_manager")
    def action_cancel(cls, order_id):
        cls.write(order_id, {"state": "cancelled"})
        return True