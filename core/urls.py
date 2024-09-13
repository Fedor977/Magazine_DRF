from django.urls import path

from .views import ProductListCreate, ProductRetrieveUpdateDestroy, OrderListCreate, OrderRetrieveUpdateDestroy, \
    CustomAuthToken, UserCreate, Logout

urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='product-list-create'),
    path('products/<slug:slug>/', ProductRetrieveUpdateDestroy.as_view(), name='product-detail'),
    path('orders/', OrderListCreate.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroy.as_view(), name='order-detail'),
    path('auth/', CustomAuthToken.as_view(), name='auth'),
    path('registration/', UserCreate.as_view(), name='registration'),
    path('logout/', Logout.as_view(), name='logout'),
]

