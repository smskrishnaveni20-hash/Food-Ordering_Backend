from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import *
from Restaurants.models import Restaurants
from Dishes.models import Dishes
from Order.models import Cart, Payment

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

class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer

# Dishes
class DishesView(generics.ListCreateAPIView):
    serializer_class = DishSerializer
    def get_queryset(self):
        return Dishes.objects.filter(restaurant__isnull=False)

class DishesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer

# Cart
class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ViewCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class ClearCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)

# Payments
class MakePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, payment_status="Success")

class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)