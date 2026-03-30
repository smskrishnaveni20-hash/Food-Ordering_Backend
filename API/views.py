from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import  APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework import generics 
from rest_framework import status
from .serializers import LoginSerializer

# Create your views here.



class LoginView( APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class RestaurantView(generics.ListCreateAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer
    
class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurants.objects.all()
    serializer_class = RestaurantSerializer

class DishesView(generics.ListCreateAPIView):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer

class DishesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dishes.objects.all()
    serializer_class = DishSerializer

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes=[IsAuthenticated]
    
    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

class ViewCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class ClearCartView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def delete(self, request):
        Cart.objects.filter(user= request.user).delete()
        return Response(
            {"message": "Cart cleared"},
            status= status.HTTP_204_NO_CONTENT
        )

class MakePaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user = self.request.user,
            payment_status = "Success"
        )

class PaymentHistoryView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user = self.request.user)