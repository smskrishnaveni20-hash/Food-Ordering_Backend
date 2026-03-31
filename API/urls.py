from django.urls import path
from .views import * 

urlpatterns = [
    path('api/v1/user/',RegisterView.as_view(),name='register'),
    path("api/v1/login/", LoginView.as_view(), name="login"),
    path('api/v1/restaurants/', RestaurantView.as_view(), name='restaurants'),
    path('api/v1/restaurants/<int:pk>', RestaurantDetailView.as_view(), name='restaurants'),
    path('api/v1/dishes/', DishesView.as_view(), name='dishes'),
    path('api/v1/dishes/<int:pk>', DishesDetailView.as_view(), name='dishes'),
    path('api/v1/payment',MakePaymentView.as_view(), name='payment'),
    path('api/v1/hist', PaymentHistoryView.as_view(),name= 'allpayments'),
    path('api/v1/add/', AddToCartView.as_view(),name='cart'),
    path('api/v1/view/',ViewCartView.as_view(),name='cart'),
    path('api/v1/clear/',ClearCartView.as_view(),name='cart'),
] 