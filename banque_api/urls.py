from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Petite route test
def home(request):
    return HttpResponse("API Banque active sur Render 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),

    # Route principale
    path('', home),

    # 👉 TES APIs ICI
    path('api/accounts/', include('accounts.urls')),
]