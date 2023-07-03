from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from config import settings
from .api import router

schema_view = get_schema_view(
    openapi.Info(
        title="Shopping API",
        default_version='v1',
        description="Backend API for Shopping",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include('account.urls')),
    path("seller/", include('seller.urls')),
    path("product/images/", include('product.urls')),
    path("product/", include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
