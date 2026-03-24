from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Product, Shipment
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ShipmentReadSerializer,
    ShipmentWriteSerializer,
)
from .pagination import StandardResultsSetPagination


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD de categorías. Escritura requiere autenticación JWT."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD de productos. Escritura requiere autenticación JWT."""
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    # Filtrado exacto por campos
    filterset_fields = ['category', 'is_active']
    # Búsqueda de texto libre
    search_fields = ['name', 'description']
    # Ordenamiento permitido
    ordering_fields = ['name', 'price', 'stock', 'created_at']
    ordering = ['-created_at']


class ShipmentViewSet(viewsets.ModelViewSet):
    """
    API de envíos.
    - Usuarios autenticados: solo lectura de sus propios envíos.
    - Staff/Admin: CRUD completo sobre todos los envíos.
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['status', 'courier_company']
    search_fields = ['tracking_number', 'courier_company', 'product__name']
    ordering_fields = ['created_at', 'estimated_delivery', 'status']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        qs = Shipment.objects.select_related('user', 'product')
        if user.is_staff or user.is_superuser:
            return qs.all()
        return qs.filter(user=user)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return ShipmentWriteSerializer
        return ShipmentReadSerializer
