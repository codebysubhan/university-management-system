from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="University API",
      default_version='v1',
      description="University Management System API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('custom_user_app.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

