from django.contrib import admin
from django.urls import path, include

# Static settings
from django.conf import settings
from django.conf.urls.static import static

# Swagger UI
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="Application API",
      default_version='v1',
      description="Application API v1",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('auth_app.urls')),
    path('api/v1/course/', include('course_app.urls')),
    path('api/v1/diplom/', include('diplom_app.urls')),
    path('api/v1/apply/', include('apply_app.urls')),

    # Swagger
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)