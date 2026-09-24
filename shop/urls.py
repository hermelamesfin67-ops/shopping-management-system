from django.urls import path
from .views import( CategoryListCReateView,
      ProductListCreateView,CategoryView,ProductView,CartListCreateView,CartView,AddToCartView,CheckoutView
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
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
