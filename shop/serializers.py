from rest_framework import serializers
from .models import Product, Category, Cart, User, CartItem,Order,OrderItem,Payment

class UserSerializer(serializers.ModelSerializer):
    role=serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'created_at', 'updated_at','username','password']
        read_only_fields = ['id', 'email', 'role', 'created_at', 'updated_at']
        extra_kwargs = {"password": {"write_only": True}}




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at', 'imageicon']
        read_only_fields = ['created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'stock',
            'category',
            'image',
            'created_at',
            'updated_at',
            'is_available'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product', 'quantity']
        read_only_fields = ['id','cart']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Quantity must be greater than 0")
        return value

    def validate(self, attrs):
        product = attrs['product']
        quantity = attrs['quantity']
        if quantity > product.stock:
            raise serializers.ValidationError({"quantity":f"Stock is only {product.stock} item are available"})
        return attrs
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'total_price', 'status']
        read_only_fields = ['id',"user", 'created_at', 'updated_at', 'total_price', 'status']
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price']
        read_only_fields = ['id', 'order', 'product', 'quantity', 'price']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'created_at', 'updated_at', 'amount', 'status', 'transaction_id','tx_ref']
        read_only_fields = ['id', 'created_at', 'updated_at', 'amount', 'status','tx_ref', 'transaction_id']