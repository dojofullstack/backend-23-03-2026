from rest_framework import serializers

from .models import Category, Product, Shipment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'stock',
            'category',
            'category_name',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


# ── Shipment ──────────────────────────────────────────────────────────────────

VALID_TRANSITIONS = {
    Shipment.Status.PENDING: [Shipment.Status.SHIPPED],
    Shipment.Status.SHIPPED: [Shipment.Status.DELIVERED],
    Shipment.Status.DELIVERED: [],
}


class ShipmentReadSerializer(serializers.ModelSerializer):
    """Serializer de solo lectura para usuarios finales."""
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Shipment
        fields = [
            'id',
            'product',
            'product_name',
            'user_email',
            'courier_company',
            'tracking_number',
            'estimated_delivery',
            'status',
            'status_display',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class ShipmentWriteSerializer(serializers.ModelSerializer):
    """Serializer de escritura para staff/admin. Valida transiciones de estado."""

    class Meta:
        model = Shipment
        fields = [
            'id',
            'user',
            'product',
            'courier_company',
            'tracking_number',
            'estimated_delivery',
            'status',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_status(self, new_status):
        """Impide retroceder el estado del envío."""
        if self.instance:
            current = self.instance.status
            allowed = VALID_TRANSITIONS.get(current, [])
            if new_status != current and new_status not in allowed:
                raise serializers.ValidationError(
                    f'Transición inválida: {current} → {new_status}. '
                    f'Transiciones permitidas: {allowed or ["ninguna"]}'
                )
        return new_status
