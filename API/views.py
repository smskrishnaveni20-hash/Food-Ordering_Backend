from django.contrib.auth.models import User
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from Dishes.models import Dishes
from Order.models import Cart, Payment
from Restaurants.models import Restaurants


# ------------------------
# AUTH VIEWS
# ------------------------

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# ------------------------
# RESTAURANTS
# ------------------------

class RestaurantView(generics.ListCreateAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer


# ------------------------
# DISHES
# ------------------------

class DishesView(generics.ListCreateAPIView):
    serializer_class = DishSerializer

    def get_queryset(self):
        # Safe: filters out any dishes with broken foreign keys
        return Dishes.objects.filter(restaurant__isnull=False)

    def perform_create(self, serializer):
        # Optional: prevent broken relationships
        serializer.save()


class DishesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DishSerializer

    def get_queryset(self):
        return Dishes.objects.filter(restaurant__isnull=False)


# ------------------------
# CART
# ------------------------

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


# ------------------------
# PAYMENT
# ------------------------

class MakePaymentView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            payment_status="Success"
        )


class PaymentHistoryView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


# ------------------------
# TEMPORARY TEST VIEW (for debugging / 500 errors)
# ------------------------
# Use this to check if dishes are serializable before hitting frontend
@api_view(['GET'])
def test_dishes(request):
    dishes = list(Dishes.objects.all().values())
    return Response(dishes)