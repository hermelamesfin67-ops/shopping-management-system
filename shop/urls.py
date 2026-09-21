from django.urls import path
from .views import( CategoryListCReateView,
      ProductListCreateView,CategoryView,ProductView,CartListCreateView,CartView
)

urlpatterns = [

  path('product/',ProductListCreateView.as_view(),name='Product'),
  path('category/', CategoryListCReateView.as_view(),name='Category'),
  path("category/<int:pk>",CategoryView.as_view(),name='Category'),
  path('product/<int:pk>',ProductView.as_view(),name='Product'),
  path('cart/',CartListCreateView.as_view(),name='Cart'),
  path('cart/<int:pk>',CartView.as_view(),name='Cart'),
  
]
