from django.test import TestCase

from checkout.models import OrderLineItem, Order


class TestCheckoutModels(TestCase):
    fixtures = ['profiles/fixtures/sample_fixtures.json', ]

    def test_order_str(self):
        order = Order.objects.filter().first()
        self.assertEqual(str(order),
                         (f'{order.order_number} - {order.profile}'))

    def test_order_line_item_str(self):
        order_item = OrderLineItem.objects.filter().first()
        self.assertEqual(str(order_item),
                         (f'Order no: {order_item.order.order_number} - '
                          f'Item: {order_item.lesson.lesson_name}'))
