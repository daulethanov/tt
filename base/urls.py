from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Тз",
        default_version='v0.0.1',
    ),
    public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("frontend.urls")),
    path("api/", include('api.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
