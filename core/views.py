from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Product, Order, Payment
from .serializers import ProductSerializer, OrderSerializer, PaymentSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from django.contrib.auth import logout, login
from django.contrib.auth import get_user_model
from .serializers import CustomUserSerializer


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # требуем аутентификацию для создания заказа

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class PaymentCreate(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer




User = get_user_model() # используется для получения модели пользователя, без необходимости создавать модельку пользователя в models

class CustomAuthToken(ObtainAuthToken):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email
        })

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

class Logout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
