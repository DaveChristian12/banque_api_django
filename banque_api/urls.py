from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Banque",
        default_version='v1',
        description="API bancaire",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

def home(request):
    html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Accueil API Banque</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f3f4f6; color: #111827; margin: 0; padding: 20px; }
        .container { max-width: 820px; margin: auto; background: white; border-radius: 14px; padding: 30px; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08); }
        h1 { margin-top: 0; }
        a { color: #2563eb; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .links { margin-top: 20px; }
        .links li { margin-bottom: 10px; }
        .note { background: #eef2ff; border-left: 4px solid #6366f1; padding: 14px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Accueil - API Banque</h1>
        <p>Bienvenue sur l’API bancaire. Tu peux accéder à l’interface de gestion des comptes en cliquant sur le lien ci-dessous.</p>

        <div class="links">
            <ul>
                <li><strong>Interface client :</strong> <a href="/api/accounts/ui/">/api/accounts/ui/</a></li>
                <li><strong>Liste des comptes / création :</strong> <a href="/api/accounts/">/api/accounts/</a></li>
                <li><strong>Swagger :</strong> <a href="/swagger/">/swagger/</a></li>
                <li><strong>Redoc :</strong> <a href="/redoc/">/redoc/</a></li>
            </ul>
        </div>

        <div class="note">
            <strong>Étapes pour accéder à la page d’accueil :</strong>
            <ol>
                <li>Démarre ton serveur Django : <code>python manage.py runserver</code></li>
                <li>Ouvre un navigateur</li>
                <li>Va à : <code>http://localhost:8000/</code></li>
            </ol>
        </div>
    </div>
</body>
</html>"""
    return HttpResponse(html, content_type='text/html')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),

    path('api/accounts/', include('accounts.urls')),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]