from models.sale import SaleOrder


class SaleOrderDiscount(SaleOrder):
    """توسعة لـ SaleOrder: بتضيف خصم على الإجمالي."""

    @classmethod
    def compute_total(cls, order_id):
        total = super().compute_total(order_id)        # الحساب الأصلي
        discount = cls.browse(order_id)["discount"]    # نسبة الخصم
        return total - (total * discount / 100)