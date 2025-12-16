from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from restaurant.models import Menu
from restaurant.serializers import MenuSerializer


class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(
            title="IceCream",
            price=80,
            inventory=100
        )
        self.assertEqual(str(item), "IceCream: 80")

class MenuViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='Helloworld#123'
        )

        # Force authentication
        self.client.force_authenticate(user=self.user)

        Menu.objects.create(title="Pizza", price=12, inventory=50)
        Menu.objects.create(title="Burger", price=8, inventory=30)
        Menu.objects.create(title="Pasta", price=10, inventory=40)

    def test_getall(self):
        response = self.client.get('/restaurant/menu/')
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
