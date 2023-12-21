from django.urls import path
from django.contrib import admin
from ShopAPI import views
from ShopAPI.views import HomeView, UserRegistrationView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.urls.converters import UUIDConverter
# urls.py




schema_view = get_schema_view(
    openapi.Info(
        title="E-Commerce API",
        default_version="v1",
        description="API for managing an e-commerce platform.",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="202020041@psu.palawan.edu.ph"),
        license=openapi.License(name="MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

class UuidConverter(UUIDConverter):
    regex = r'[0-9a-f-]+'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # Users
    path('api/register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('api/users/', views.UserProfileListView.as_view(), name='user-view'),

    path('admin/', admin.site.urls),  # Include this line for the admin URLs
    
    # Orders
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    
    # Cart Items
    path('cart_items/', views.CartItemListView.as_view(), name='cartitem-list-create'),
    path('cart_items/create/', views.CartItemCreateView.as_view(), name='cartitem-create'),
    path('cart_items/<int:pk>/', views.CartItemDetailView.as_view(), name='cartitem-detail'),
    path('cart_items/<int:pk>/delete/', views.CartItemDeleteView.as_view(), name='cartitem-delete'),
    
    # Checkout
    path('checkout/', views.OrderListView.as_view(), name='checkout'),
    
    # Products
    path('api/products/', views.ProductListView.as_view(), name='product-list'),
    path('api/products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('api/products/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('api/products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
    
    # Add more patterns for other endpoints
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)