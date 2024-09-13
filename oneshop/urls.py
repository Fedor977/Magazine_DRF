from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('auth/', auth_views.obtain_auth_token)
]

urlpatterns += doc_urls
