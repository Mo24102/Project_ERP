from Core.orm import Model
from Core.exceptions import UserError, AccessError
from Core.security import Env
from models.product import Product, Partner
from models.sale import SaleOrderLine
from models.sale_discount import SaleOrderDiscount as SaleOrder


def main():
    Model.load_all()

    # 1) بيانات أساسية
    laptop = Product.create({"name": "Laptop", "price": 15000})
    mouse = Product.create({"name": "Mouse", "price": 300})
    customer = Partner.create({"name": "Ahmed", "city": "Cairo"})

    # 2) أمر بيع بخصم 10%
    order = SaleOrder.create({"partner_id": customer, "discount": 10})
    SaleOrderLine.create({"order_id": order, "product_id": laptop, "qty": 2})
    SaleOrderLine.create({"order_id": order, "product_id": mouse, "qty": 5})

    print("Total after discount:", SaleOrder.compute_total(order))

    # 3) تأكيد الأمر
    SaleOrder.action_confirm(order)
    print("State:", SaleOrder.browse(order)["state"])

    # 4) اختبار الصلاحيات
    Env.user = "ali"
    try:
        SaleOrder.action_cancel(order)
    except AccessError as e:
        print("Access denied:", e)

    # 5) اختبار الأخطاء
    Env.user = "admin"
    try:
        Product.create({"name": "Bad", "price": -5})
    except UserError as e:
        print("Error:", e)

    # 6) بحث بالـ domain
    confirmed = SaleOrder.search([("state", "=", "confirmed")])
    print("Confirmed orders:", confirmed)

    Model.save_all()


if __name__ == "__main__":
    main()