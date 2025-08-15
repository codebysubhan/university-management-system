from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from custom_user_app.views import GoogleLogin

schema_view = get_schema_view(
    openapi.Info(
        title="University API",
        default_version='v1',
        description="University Management System API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('accounts/', include("allauth.urls")),  # mostly for debugging allauth
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    # Social login
    path('api/auth/social/google/', GoogleLogin.as_view(), name='google_login'),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App endpoints
    path('', include('custom_user_app.urls')),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# Swagger JWT settings
from django.conf import settings
if not hasattr(settings, 'SWAGGER_SETTINGS'):
    settings.SWAGGER_SETTINGS = {}

settings.SWAGGER_SETTINGS.update({
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header. Example: "Bearer {token}"'
        }
    }
})
