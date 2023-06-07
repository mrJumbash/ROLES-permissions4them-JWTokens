from django.urls import path
from accounts import views

urlpatterns = [
    path("set/tenant/", views.TenantSetAPI.as_view()),
    path("register/buyer/", views.RegistrationBuyerAPI.as_view()),
    path("register/admin/", views.RegistrationAdminAPI.as_view()),
    path("register/confirm/", views.ConfirmAPIView.as_view()),
    path("login/", views.LoginAPI.as_view()),
]
