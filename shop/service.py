from .models import Cart, CartItem


def  add_to_cart(user, product, quantity):
    
  try:
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity)
        return cart_item
  except Cart.DoesNotExist:
        cart = Cart.objects.create(user=user)
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity)
        return cart_item
  