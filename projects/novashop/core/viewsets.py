from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from .models import User, Category, Product, Cart, Order, Review
from .serializers import UserSerializer, CategorySerializer, ProductSerializer, CartSerializer, OrderSerializer, ReviewSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'user_list'
        users = cache.get(cache_key)

        if not users:
            users = super().list(request, *args, **kwargs).data
            cache.set(cache_key, users, timeout=60*15)

        return Response(users)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'category_list'
        categories = cache.get(cache_key)

        if not categories:
            categories = super().list(request, *args, **kwargs).data
            cache.set(cache_key, categories, timeout=60*15)

        return Response(categories)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'product_list'
        products = cache.get(cache_key)

        if not products:
            products = super().list(request, *args, **kwargs).data
            cache.set(cache_key, products, timeout=60*15)

        return Response(products)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'cart_list'
        carts = cache.get(cache_key)

        if not carts:
            carts = super().list(request, *args, **kwargs).data
            cache.set(cache_key, carts, timeout=60*15)

        return Response(carts)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'order_list'
        orders = cache.get(cache_key)

        if not orders:
            orders = super().list(request, *args, **kwargs).data
            cache.set(cache_key, orders, timeout=60*15)

        return Response(orders)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'review_list'
        reviews = cache.get(cache_key)

        if not reviews:
            reviews = super().list(request, *args, **kwargs).data
            cache.set(cache_key, reviews, timeout=60*15)

        return Response(reviews)

