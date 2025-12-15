from dataclasses import dataclass
import unittest

@dataclass
class Order:
    order_id: int
    product_name: str
    quantity: int
    price: float

class ValidationError(Exception):
    pass

def validate_order(func):
    def wrapper(order: Order, *args, **kwargs):

        if not isinstance(order.order_id, int) or order.order_id <= 0:
            raise ValidationError("order_id має бути додатним цілим числом")

        if not isinstance(order.product_name, str) or not order.product_name.strip():
            raise ValidationError("product_name має бути непорожнім рядком")

        if not isinstance(order.quantity, int) or order.quantity <= 0:
            raise ValidationError("quantity має бути додатним цілим числом")

        if not isinstance(order.price, (int, float)) or order.price <= 0:
            raise ValidationError("price має бути додатним числом")

        return func(order, *args, **kwargs)

    return wrapper

@validate_order
def process_order(order: Order) -> float:
    return order.quantity * order.price

class TestOrderValidation(unittest.TestCase):

    def test_valid_order(self):
        order = Order(1, "Phone", 2, 500.0)
        self.assertEqual(process_order(order), 1000.0)

    def test_invalid_id(self):
        order = Order(0, "Phone", 2, 500.0)
        with self.assertRaises(ValidationError):
            process_order(order)

    def test_empty_name(self):
        order = Order(1, "", 2, 500.0)
        with self.assertRaises(ValidationError):
            process_order(order)

    def test_negative_quantity(self):
        order = Order(1, "Phone", -1, 500.0)
        with self.assertRaises(ValidationError):
            process_order(order)

    def test_invalid_price(self):
        order = Order(1, "Phone", 2, -10.0)
        with self.assertRaises(ValidationError):
            process_order(order)
            
if __name__ == "__main__":
    unittest.main()

