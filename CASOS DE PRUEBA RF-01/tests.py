from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Stock


class ViewStockIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='tester-pass')
        self.category = Category.objects.create(group='Integration Test')
        for item_name in ['Item A', 'Item B', 'Item C', 'Item D', 'Item E']:
            Stock.objects.create(
                category=self.category,
                item_name=item_name,
                quantity=10,
                date=timezone.now(),
            )

    def test_view_stock_returns_created_items(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('view_stock'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'stock/view_stock.html')
        self.assertIn('everything', response.context)
        self.assertEqual(len(response.context['everything']), 5)
        self.assertQuerySetEqual(
            response.context['everything'].order_by('item_name'),
            ['Item A', 'Item B', 'Item C', 'Item D', 'Item E'],
            transform=lambda stock: stock.item_name,
        )
