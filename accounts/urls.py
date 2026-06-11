from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccountListCreateView.as_view()),
    path('health/', views.HealthCheckView.as_view()),
    path('ui/', views.AccountInterfaceView.as_view()),
    path('<uuid:account_id>/', views.AccountDetailView.as_view()),
    path('<uuid:account_id>/deposit/', views.DepositView.as_view()),
    path('<uuid:account_id>/withdraw/', views.WithdrawView.as_view()),
]