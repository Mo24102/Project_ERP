import pytest
from Core.orm import Model
from Core.security import Env
from Core.exceptions import UserError, AccessError
from models.product import Product
from models.sale import SaleOrderLine
from models.sale_discount import SaleOrderDiscount as SaleOrder


@pytest.fixture(autouse=True)
def clean_db():
    Model._store = {}
    Env.user = "admin"


def make_order(discount=0):
    p = Product.create({"name": "Pen", "price": 100})
    o = SaleOrder.create({"discount": discount})
    SaleOrderLine.create({"order_id": o, "product_id": p, "qty": 3})
    return o


def test_total_without_discount():
    assert SaleOrder.compute_total(make_order()) == 300


def test_total_with_discount():
    assert SaleOrder.compute_total(make_order(discount=10)) == 270


def test_confirm_changes_state():
    o = make_order()
    SaleOrder.action_confirm(o)
    assert SaleOrder.browse(o)["state"] == "confirmed"


def test_cannot_confirm_empty_order():
    o = SaleOrder.create({})
    with pytest.raises(UserError):
        SaleOrder.action_confirm(o)


def test_sales_user_cannot_cancel():
    o = make_order()
    Env.user = "ali"
    with pytest.raises(AccessError):
        SaleOrder.action_cancel(o)