from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.generic import CreateView
from django.views.decorators.http import require_POST, require_http_methods
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Order, CartItem, Product, UserProfile
from .serializers import (
    OrderSerializer,
    CartItemSerializer,
    ProductSerializer,
    UserSerializer,
    UserProfileSerializer,
    LoginSerializer,
    CartItemCreateSerializer,
)

class HomeView(TemplateView):
    template_name = 'home.html'
    
# Views for Orders
class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

# Views for Cart Items
class CartItemListView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

class CartItemCreateView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = self.get_or_create_pending_order()
        serializer.save(order=order)

    def get_or_create_pending_order(self):
        user = self.request.user
        pending_order = Order.objects.filter(user=user, status=Order.PENDING).first()

        if not pending_order:
            pending_order = Order.objects.create(user=user, status=Order.PENDING)

        return pending_order
    
class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer  # Replace with your CartItem serializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        order = instance.order
        total_amount = order.total_amount

        # Assuming the price is stored in the CartItem model as 'price'
        if instance.price is not None:
            item_price = instance.price * instance.quantity

            # Decrease the total amount by the price of the item being removed
            order.total_amount = total_amount - item_price
            order.save()
        else:
            # Handle the case where price is None (or any default behavior you want)
            item_price = 0
            # You might want to log a warning or handle it in some way

        self.perform_destroy(instance)
        return Response({'detail': 'Item removed from cart successfully.'}, status=status.HTTP_204_NO_CONTENT)

class CheckedOutItemsView(generics.ListAPIView):
    queryset = Order.objects.filter(status=1)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

# Views for Products
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Replace with your Product serializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Replace with your Product serializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

# User registration view
class UserRegistrationView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()  # This queryset is not used, but it's required for generics.CreateAPIView
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# User profile views
class UserProfileListView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

class UserProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
