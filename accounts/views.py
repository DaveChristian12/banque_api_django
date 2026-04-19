from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Account
from .serializers import AccountSerializer
from decimal import Decimal

# ========================
# 0. Health Check (no DB required)
# ========================
class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "API is running ✅"}, status=status.HTTP_200_OK)

# ========================
# 1. Lister et Créer des comptes
# ========================
class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        
        return Response({
            "message": "Compte créé avec succès",
            "account": serializer.data
        }, status=status.HTTP_201_CREATED)


# ========================
# 2. Dépôt sur un compte
# ========================
class DepositView(APIView):
    def post(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        amount = request.data.get('amount')

        try:
            amount = Decimal(str(amount))
            if amount <= 0:
                return Response({"error": "Le montant doit être positif"}, status=status.HTTP_400_BAD_REQUEST)
            
            new_balance = account.deposit(amount)
            
            return Response({
                "message": f"Dépôt de {amount} € effectué avec succès",
                "account_id": str(account.id),
                "new_balance": new_balance
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ========================
# 3. Retrait d'un compte
# ========================
class WithdrawView(APIView):
    def post(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        amount = request.data.get('amount')

        try:
            amount = Decimal(str(amount))
            if amount <= 0:
                return Response({"error": "Le montant doit être positif"}, status=status.HTTP_400_BAD_REQUEST)
            
            new_balance = account.withdraw(amount)
            
            return Response({
                "message": f"Retrait de {amount} € effectué avec succès",
                "account_id": str(account.id),
                "new_balance": new_balance
            }, status=status.HTTP_200_OK)
            
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ========================
# 4. Détail d'un compte (optionnel mais utile)
# ========================
class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'