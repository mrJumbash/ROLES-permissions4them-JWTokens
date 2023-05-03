from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from core.settings.yasg import urlpatterns as jazzmin_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.feed.urls")),
    path("api/v1/", include("api.users.urls")),
]
urlpatterns += jazzmin_urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
