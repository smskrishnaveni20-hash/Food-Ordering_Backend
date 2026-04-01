from django.urls import path
from .views import * 

urlpatterns = [
    # Authentication
    path('api/v1/user/', RegisterView.as_view(), name='register'),
    path('api/v1/login/', LoginView.as_view(), name='login'),

    # Restaurants
    path('api/v1/restaurants/', RestaurantView.as_view(), name='restaurants-list'),
    path('api/v1/restaurants/<int:pk>/', RestaurantDetailView.as_view(), name='restaurants-detail'),

    # Dishes
    path('api/v1/dishes/', DishesView.as_view(), name='dishes-list'),
    path('api/v1/dishes/<int:pk>/', DishesDetailView.as_view(), name='dishes-detail'),

    # Cart
    path('api/v1/cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('api/v1/cart/view/', ViewCartView.as_view(), name='cart-view'),
    path('api/v1/cart/clear/', ClearCartView.as_view(), name='cart-clear'),

    # Payment
    path('api/v1/payment/make/', MakePaymentView.as_view(), name='payment-make'),
    path('api/v1/payment/history/', PaymentHistoryView.as_view(), name='payment-history'),
]