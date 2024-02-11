from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ItemInventory
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .serializers import ItemInventorySerializer

class KaiznTaskTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.item1 = ItemInventory.objects.create(
            user_id=self.user.id,
            sku="SKU001",
            name="Test Item",
            tags="Tag1, Tag2",
            category="TestCategory",
            in_stock=10,
            available_stock=8
        )

        ItemInventory.objects.create(
            user_id=self.user.id,
            sku="SKU002",
            name="Test Item",
            tags="Tag1, Tag2",
            category="TestCategory",
            in_stock=10,
            available_stock=8
        )

        ItemInventory.objects.create(
            user_id=self.user.id,
            sku="SKU002",
            name="Test Item",
            tags="Tag1, Tag2",
            category="TestCategory1",
            in_stock=10,
            available_stock=8
        )


    def test_login_view(self):

        # The below test is for login pass
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

        # The below test is for login fail...
        response = self.client.post(reverse('login'), {'username': 'invaliduser', 'password': 'invalidpassword'})
        self.assertContains(response, '<p class="error-message"', status_code=200)

    def test_item_dashboard_view(self):
        # This requires authentication to be viewed if not it gets redirected
        logout(self.client)
        response = self.client.get(reverse('item_dashboard'))
        self.assertRedirects(response, '/login?next=/item_dashboard/', target_status_code=301, fetch_redirect_response=True) # It redirects to the login page

        # Test the item_dashboard view with an authenticated user
        self.client.force_login(self.user)
        response = self.client.get(reverse('item_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kaizn_app/item_dashboard.html')
        self.assertContains( response, '<tr class="record"', count=3 )

        # Test whether the query param works
        response = self.client.get(reverse('item_dashboard') + '?category=TestCategory')
        self.assertContains( response, '<tr class="record"', count=2 )

    def test_item_inventory_serializer(self):
        # Serialize the item
        serializer = ItemInventorySerializer(self.item1)
        serialized_data = serializer.data

        # Add your assertions based on the expected serialized data
        self.assertEqual(serialized_data['sku'], "SKU001")
        self.assertEqual(serialized_data['name'], "Test Item")

    # Add more tests as needed
