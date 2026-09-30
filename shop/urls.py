from django.urls import path
from .views import( CategoryListCReateView,
      ProductListCreateView,CategoryView,ProductView,CartListCreateView,CartView,
      PaymentCreateView,AddToCartView,CheckoutView,CartItemListView,MyLogin,UserListView,UserCreateView,UserProfileView
)
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [

  path('product/',ProductListCreateView.as_view(),name='Product'),
  path('category/', CategoryListCReateView.as_view(),name='Category'),
  path("category/<int:pk>",CategoryView.as_view(),name='Category'),
  path('product/<int:pk>',ProductView.as_view(),name='Product'),
  path('cart/',CartListCreateView.as_view(),name='Cart'),
  path('cart/<int:pk>',CartView.as_view(),name='Cart'),
  path('cart/add/',AddToCartView.as_view(),name='AddToCart'),
  path('cart/checkout/', CheckoutView.as_view(), name='checkout'),
  path('token/', MyLogin.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  path('payment/',PaymentCreateView.as_view(),name='payment'),
  path('all/cart',CartItemListView.as_view(),name='CartItem'),
  path('user/',UserListView.as_view(),name='User'),
  path('users/',UserCreateView.as_view(),name='User'),
  path("profile/",UserProfileView.as_view(),name='User'),
]

