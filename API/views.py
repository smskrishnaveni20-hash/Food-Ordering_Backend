from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from Restaurants.models import Restaurants
from Dishes.models import Dishes
from Order.models import Cart, Order, Payment
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    RestaurantSerializer,
    DishSerializer,
    CartSerializer,
    PaymentSerializer,
    OrderSerializer,
)

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

# Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

# Restaurants
class RestaurantView(generics.ListCreateAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]

class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]

# Dishes
class DishesView(generics.ListCreateAPIView):
    serializer_class = DishSerializer
    queryset = Dishes.objects.all()
    permission_classes = [IsAdminOrReadOnly]

class DishesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminOrReadOnly]

# Cart
class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dish = serializer.validated_data["dish"]
        quantity = serializer.validated_data.get("quantity", 1)

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            dish=dish,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=["quantity"])

        output_serializer = self.get_serializer(cart_item)
        headers = self.get_success_headers(output_serializer.data)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(output_serializer.data, status=status_code, headers=headers)

class ViewCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class ClearCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Orders
class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")

    def create(self, request, *args, **kwargs):
        items_data = request.data.get("items")
        if not items_data or not isinstance(items_data, list):
            return Response(
                {"error": "A non-empty 'items' list is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_price = Decimal("0.00")
        for item in items_data:
            if not isinstance(item, dict) or "dish" not in item:
                return Response(
                    {"error": "Each item must contain a 'dish' ID."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            dish_id = item["dish"]
            try:
                quantity = int(item.get("quantity", 1))
                if quantity < 1:
                    raise ValueError()
            except (ValueError, TypeError):
                return Response(
                    {"error": f"Invalid quantity for dish {dish_id}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                dish = Dishes.objects.get(id=dish_id)
            except Dishes.DoesNotExist:
                return Response(
                    {"error": f"Dish with ID {dish_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if dish.is_available is False:
                return Response(
                    {"error": f"Dish '{dish.name}' is currently unavailable."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            dish_price = Decimal(str(dish.price or 0))
            total_price += dish_price * quantity

        order = Order.objects.create(user=request.user, total_price=total_price)
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Payments
class MakePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.validated_data.get("order")
        if order and order.user != self.request.user:
            raise PermissionDenied("You do not have permission to pay for another user's order.")
        serializer.save(payment_status="Success")

class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
