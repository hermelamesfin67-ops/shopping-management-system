from .models import Cart, CartItem, Order, OrderItem
from django.db import transaction
from utils.exceptions import InsufficientStockError


@transaction.atomic
def add_to_cart(user, product, quantity):
    if quantity > product.stock:
        raise InsufficientStockError("not enough in stock")
    try:
        cart = Cart.objects.get(user=user)
        try:
            cart_item = CartItem.objects.get(
                cart=cart, product=product)
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                raise InsufficientStockError("not enough in stock")
            cart_item.quantity = new_quantity
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart, product=product, quantity=quantity)

    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity)
        return cart_item


def checkout(user):
    cart = Cart.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        raise ValueError("Cart is empty.")
    order = Order.objects.create(user=user)
    total = 0
    for cart_item in cart_items:
        product = cart_item.product

        if cart_item.quantity > product.stock:
            raise ValueError(
                f"Not enough stock for {product.name}."
            )

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=cart_item.quantity,
            price=product.price
        )
        total += product.price * cart_item.quantity
    order.total_price = total
    order.save()

    return order
