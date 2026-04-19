from django.urls import path
from . import views

urlpatterns = [
    # Health check
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    
    # Database check
    path('db/', views.DatabaseCheckView.as_view(), name='db-check'),
    
    # Liste et création de comptes
    path('', views.AccountListCreateView.as_view(), name='account-list-create'),
    
    # Dépôt
    path('<uuid:account_id>/deposit/', views.DepositView.as_view(), name='deposit'),
    
    # Retrait
    path('<uuid:account_id>/withdraw/', views.WithdrawView.as_view(), name='withdraw'),
    
    # Détail d'un compte
    path('<uuid:account_id>/', views.AccountDetailView.as_view(), name='account-detail'),
]