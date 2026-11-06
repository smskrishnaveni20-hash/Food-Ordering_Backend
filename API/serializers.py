from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from Restaurants.models import Restaurants
from Dishes.models import Dishes
from Order.models import Cart, Order, Payment
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        refresh = RefreshToken.for_user(user)
        return {
            "user": user.username,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# Restaurant serializer
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurants
        fields = "__all__"

# Dish serializer
class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = "__all__"

# Cart serializer
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        read_only_fields = ["user"]

# Order serializer
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'total_price', 'created_at']
        read_only_fields = ['id', 'total_price', 'created_at']

# Payment serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["payment_status", "created_at"]

    def validate_order(self, order):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            if order.user != request.user:
                raise PermissionDenied("You do not have permission to pay for another user's order.")
        if Payment.objects.filter(order=order).exists():
            raise serializers.ValidationError("This order has already been paid.")
        return order
