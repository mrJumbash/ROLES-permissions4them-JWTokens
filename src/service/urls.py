from django.urls import path
from service import views

urlpatterns = [
    path("products/", views.ProductAPI.as_view()),
    path("products/<uuid:id>/", views.ProductDetailAPI.as_view()),
]
