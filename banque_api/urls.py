from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger config
schema_view = get_schema_view(
    openapi.Info(
        title="API Banque",
        default_version='v1',
        description="Documentation de l'API bancaire (comptes, dépôts, retraits)",
        contact=openapi.Contact(email="dev@banque.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Page test
def home(request):
    return HttpResponse("API Banque active ")

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    # API
    path('api/accounts/', include('accounts.urls')),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]