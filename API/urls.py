from django.urls import path
from .views import * 

urlpatterns = [
    path('user/',RegisterView.as_view(),name='register'),
    path("login/", LoginView.as_view(), name="login"),
    path('restaurants/', RestaurantView.as_view(), name='restaurants'),
    path('restaurants/<int:pk>', RestaurantDetailView.as_view(), name='restaurants'),
    path('dishes/', DishesView.as_view(), name='dishes'),
    path('dishes/<int:pk>', DishesDetailView.as_view(), name='dishes'),
    path('payment',MakePaymentView.as_view(), name='payment'),
    path('hist', PaymentHistoryView.as_view(),name= 'allpayments'),
    path('add/', AddToCartView.as_view(),name='cart'),
    path('view/',ViewCartView.as_view(),name='cart'),
    path('clear/',ClearCartView.as_view(),name='cart'),
] 