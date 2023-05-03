from django.urls import path
from . import views

urlpatterns = [
    path("manga/", views.MangaListCreateAPI.as_view()),
    path("manga/<int:id>/", views.MangaDetailAPI.as_view()),
    path("category/", views.CategoryAPIView.as_view()),
    path("reviews/", views.ReviewListCreateAPI.as_view()),
    path("reviews/<int:id>/", views.ReviewListCreateAPI.as_view()),
]
