from django.urls import path

from social_auth.views import GoogleSocialAuthView

urlpatterns = [
    path(f"google/", GoogleSocialAuthView.as_view()),
]
