from .models import Cart, CartItem, Order, OrderItem, Payment
from django.db import transaction
from utils.exceptions import InsufficientStockError, InvalidOrderStatusError, PaymentAlreadyExistsError, PaymentInitializationError, PaymentNotFoundError
import uuid
import requests
from django.conf import settings

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


def create_payment(order):

    if order.status != 'pending':
        raise InvalidOrderStatusError(
            "Payment can only be made for a pending order."
        )

    if hasattr(order, 'payment'):
        raise PaymentAlreadyExistsError(
            "Payment already exists for this order."
        )

    # transaction reference create
    tx_ref = f"ORDER-{order.id}-{uuid.uuid4().hex[:8]}"

    payment = Payment.objects.create(
        order=order,
        amount=order.total_price,
        tx_ref=tx_ref
    )

    url = "https://api.chapa.global/v2/payments/hosted"
    amount_in_cents = int(order.total_price * 100)

    payload = {
        "amount": str(amount_in_cents),
        "currency": "ETB",
        "tx_ref": tx_ref,
    }

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )
    if response.status_code != 200:
        print("Chapa status:", response.status_code)
        print("Chapa response:", response.text)

        raise PaymentInitializationError(
            "Unable to initialize payment with Chapa."
        )
    data = response.json()
    if data.get("status") != "success":
        raise PaymentInitializationError(
            "Chapa payment initialization failed."
        )

    return payment, data
