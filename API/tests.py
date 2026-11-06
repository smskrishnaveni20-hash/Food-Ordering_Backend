from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from Dishes.models import Dishes
from Order.models import Cart, Order, Payment
from Restaurants.models import Restaurants


class APITestSuite(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a restaurant
        self.restaurant = Restaurants.objects.create(
            Restaurant_Name="Test Bistro",
            Restaurant_Location="123 Test St",
            Mobile_Number="+919876543210",
            Url_Offical="https://testbistro.com",
            Rating=Decimal("4.5"),
        )

        # Create dishes
        self.dish1 = Dishes.objects.create(
            restaurants=self.restaurant,
            name="Chicken Biriyani",
            price=250,
            is_available=True,
            Available_in="Test Bistro",
        )
        self.dish2 = Dishes.objects.create(
            restaurants=self.restaurant,
            name="Mutton Mandi",
            price=350,
            is_available=True,
            Available_in="Test Bistro",
        )
        self.unavailable_dish = Dishes.objects.create(
            restaurants=self.restaurant,
            name="Unavailable Salmon",
            price=500,
            is_available=False,
            Available_in="Test Bistro",
        )

        # Create primary test user
        self.user1_password = "SuperSecurePassword123!@"
        self.user1 = User.objects.create_user(
            username="user_one",
            email="user_one@example.com",
            password=self.user1_password,
        )

        # Create secondary test user
        self.user2_password = "SuperSecurePassword456!@"
        self.user2 = User.objects.create_user(
            username="user_two",
            email="user_two@example.com",
            password=self.user2_password,
        )

    def test_register_weak_password_rejected(self):
        """Registering with a weak password (e.g. too short/common) should fail with 400."""
        payload = {
            "username": "new_weak_user",
            "email": "weak@example.com",
            "password": "123",
        }
        response = self.client.post("/api/v1/user/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_success_no_hash_in_response(self):
        """Registering with a valid password succeeds; response contains username and email, never password or hash."""
        payload = {
            "username": "new_strong_user",
            "email": "strong@example.com",
            "password": "StrongPassword999!#@",
        }
        response = self.client.post("/api/v1/user/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("username"), "new_strong_user")
        self.assertEqual(response.data.get("email"), "strong@example.com")
        self.assertNotIn("password", response.data)
        self.assertNotIn("pbkdf2", str(response.data))
        self.assertNotIn("argon2", str(response.data))

    def test_login(self):
        """Logging in with valid credentials returns user, access token, and refresh token."""
        payload = {
            "username": "user_one",
            "password": self.user1_password,
        }
        response = self.client.post("/api/v1/login/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data.get("user"), "user_one")

    def test_public_get_restaurants_and_dishes(self):
        """GET /api/v1/restaurants/ and /api/v1/dishes/ should be publicly accessible without authentication."""
        res_restaurants = self.client.get("/api/v1/restaurants/")
        self.assertEqual(res_restaurants.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res_restaurants.data), 1)

        res_dishes = self.client.get("/api/v1/dishes/")
        self.assertEqual(res_dishes.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res_dishes.data), 1)

    def test_unauthenticated_post_dishes_returns_401_or_403(self):
        """Unauthenticated POST to dishes must be rejected with 401 or 403."""
        payload = {
            "name": "Hacker Dish",
            "price": 999,
            "restaurants": self.restaurant.id,
            "is_available": True,
        }
        response = self.client.post("/api/v1/dishes/", payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_cart_add_twice_gives_one_row_with_summed_quantity(self):
        """Adding the same dish to the cart multiple times sums the quantity in a single row."""
        self.client.force_authenticate(user=self.user1)

        payload1 = {"dish": self.dish1.id, "quantity": 2}
        res1 = self.client.post("/api/v1/cart/add/", payload1, format="json")
        self.assertIn(res1.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

        payload2 = {"dish": self.dish1.id, "quantity": 3}
        res2 = self.client.post("/api/v1/cart/add/", payload2, format="json")
        self.assertIn(res2.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])

        rows = Cart.objects.filter(user=self.user1, dish=self.dish1)
        self.assertEqual(rows.count(), 1)
        self.assertEqual(rows.first().quantity, 5)

    def test_create_order_total_computed_server_side(self):
        """Order total must be computed on the server from Dishes.price, ignoring any client-sent price."""
        self.client.force_authenticate(user=self.user1)

        # dish1 = 250 (qty 2 = 500), dish2 = 350 (qty 1 = 350) -> total = 850.00
        payload = {
            "items": [
                {"dish": self.dish1.id, "quantity": 2},
                {"dish": self.dish2.id, "quantity": 1},
            ],
            "total_price": 10.00,  # spoofed client total, should be ignored
        }
        response = self.client.post("/api/v1/orders/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(Decimal(str(response.data["total_price"])), Decimal("850.00"))

        created_order = Order.objects.get(id=response.data["id"])
        self.assertEqual(created_order.total_price, Decimal("850.00"))
        self.assertEqual(created_order.user, self.user1)

        # Test rejection of unavailable dish
        bad_payload = {
            "items": [{"dish": self.unavailable_dish.id, "quantity": 1}]
        }
        bad_res = self.client.post("/api/v1/orders/", bad_payload, format="json")
        self.assertEqual(bad_res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pay_own_order_succeeds(self):
        """Paying for one's own order succeeds and sets status to Success."""
        self.client.force_authenticate(user=self.user1)
        order = Order.objects.create(user=self.user1, total_price=Decimal("500.00"))

        payload = {
            "order": order.id,
            "payment_method": "COD",
        }
        response = self.client.post("/api/v1/payment/make/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment = Payment.objects.get(order=order)
        self.assertEqual(payment.payment_status, "Success")
        self.assertEqual(payment.payment_method, "COD")

    def test_pay_another_user_order_fails(self):
        """Paying for another user's order must be rejected with 403 or 400."""
        # Order belongs to user1
        order = Order.objects.create(user=self.user1, total_price=Decimal("500.00"))

        # user2 attempts payment
        self.client.force_authenticate(user=self.user2)
        payload = {
            "order": order.id,
            "payment_method": "CARD",
        }
        response = self.client.post("/api/v1/payment/make/", payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST])
        self.assertFalse(Payment.objects.filter(order=order).exists())

    def test_payment_history_returns_only_own_payments(self):
        """GET /api/v1/payment/history/ should only return payments belonging to the authenticated user."""
        order1 = Order.objects.create(user=self.user1, total_price=Decimal("100.00"))
        Payment.objects.create(order=order1, payment_method="GPAY", payment_status="Success")

        order2 = Order.objects.create(user=self.user2, total_price=Decimal("200.00"))
        Payment.objects.create(order=order2, payment_method="PHONEPE", payment_status="Success")

        # As user1
        self.client.force_authenticate(user=self.user1)
        response1 = self.client.get("/api/v1/payment/history/")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        order_ids1 = [p["order"] for p in response1.data]
        self.assertIn(order1.id, order_ids1)
        self.assertNotIn(order2.id, order_ids1)

        # As user2
        self.client.force_authenticate(user=self.user2)
        response2 = self.client.get("/api/v1/payment/history/")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        order_ids2 = [p["order"] for p in response2.data]
        self.assertIn(order2.id, order_ids2)
        self.assertNotIn(order1.id, order_ids2)
