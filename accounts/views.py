from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from .models import Account
from .serializers import AccountSerializer
from decimal import Decimal

# ========================
# 0. Health Check (no DB required)
# ========================
class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "API is running "}, status=status.HTTP_200_OK)

# ========================
# 0b. Database Check
# ========================
class DatabaseCheckView(APIView):
    def get(self, request):
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({
                "status": "Database is connected ",
                "database": connection.settings_dict.get('ENGINE', 'unknown')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "Database connection failed ❌",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ========================
# 0c. Migration Check
# ========================
class MigrationCheckView(APIView):
    def get(self, request):
        try:
            from django.db import connection
            with connection.cursor() as cursor:
                # Check if the accounts_account table exists
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='accounts_account'
                """)
                table_exists = cursor.fetchone() is not None
            
            if table_exists:
                # Try to count records
                count = Account.objects.count()
                return Response({
                    "status": "Migrations have run ",
                    "table_exists": True,
                    "account_count": count
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": "Table does not exist ",
                    "table_exists": False,
                    "message": "Run 'python manage.py migrate' to create tables"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            import traceback
            return Response({
                "status": "Migration check failed ",
                "error": str(e),
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ========================
# 1. Lister et Créer des comptes
# ========================
class AccountListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.all()
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            return Response({
                "error": f"Erreur lors de la récupération des comptes: {str(e)}",
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account = serializer.save()
            
            return Response({
                "message": "Compte créé avec succès",
                "account": serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            import traceback
            return Response({
                "error": f"Erreur lors de la création du compte: {str(e)}",
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class AccountInterfaceView(APIView):
    def get(self, request):
        html = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Interface API Banque</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f7f8fc; color: #202124; }
        h1, h2 { color: #111827; }
        .card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(15, 23, 42, 0.05); }
        label { display: block; margin-bottom: 6px; font-weight: 600; }
        input, button, select { width: 100%; padding: 10px 12px; border: 1px solid #cbd5e1; border-radius: 8px; margin-bottom: 12px; font-size: 14px; }
        button { width: auto; cursor: pointer; background: #2563eb; color: white; border: none; }
        button.secondary { background: #4b5563; }
        table { width: 100%; border-collapse: collapse; margin-top: 12px; }
        th, td { padding: 10px; border: 1px solid #e2e8f0; text-align: left; }
        th { background: #f1f5f9; }
        .message { padding: 12px; border-radius: 10px; margin-bottom: 20px; }
        .success { background: #dcfce7; color: #166534; }
        .error { background: #fee2e2; color: #991b1b; }
        .inline { display: inline-flex; gap: 8px; align-items: center; }
    </style>
</head>
<body>
    <h1>Interface API Banque</h1>

    <div class="card">
        <h2>Statut</h2>
        <div id="status">Chargement...</div>
    </div>

    <div class="card">
        <h2>Comptes</h2>
        <button id="refresh">Rafraîchir la liste</button>
        <div id="accounts"></div>
    </div>

    <div class="card">
        <h2>Créer un compte</h2>
        <div id="createMessage"></div>
        <label for="holder">Nom du titulaire</label>
        <input type="text" id="holder" placeholder="Ex : Jean Dupont" />
        <label for="email">Email</label>
        <input type="email" id="email" placeholder="email@example.com" />
        <button id="createAccount">Créer</button>
    </div>

    <div class="card">
        <h2>Dépôt / Retrait</h2>
        <div id="operationMessage"></div>
        <label for="selectedAccount">Compte</label>
        <select id="selectedAccount"></select>
        <label for="amount">Montant</label>
        <input type="number" id="amount" step="0.01" min="0" placeholder="Ex : 100" />
        <div class="inline">
            <button id="deposit">Dépôt</button>
            <button id="withdraw" class="secondary">Retrait</button>
        </div>
    </div>

    <script>
        const apiBase = '/api/accounts';
        const statusEl = document.getElementById('status');
        const accountsEl = document.getElementById('accounts');
        const selectedAccount = document.getElementById('selectedAccount');
        const operationMessage = document.getElementById('operationMessage');
        const createMessage = document.getElementById('createMessage');

        async function showStatus() {
            try {
                const res = await fetch(`${apiBase}/health/`);
                const data = await res.json();
                statusEl.innerHTML = `<div class='message success'>${data.status}</div>`;
            } catch (error) {
                statusEl.innerHTML = `<div class='message error'>Erreur de connexion à l'API</div>`;
            }
        }

        async function loadAccounts() {
            accountsEl.innerHTML = 'Chargement...';
            selectedAccount.innerHTML = '';
            try {
                const res = await fetch(`${apiBase}/`);
                const accounts = await res.json();
                if (!Array.isArray(accounts)) {
                    throw new Error('Réponse inattendue');
                }
                if (accounts.length === 0) {
                    accountsEl.innerHTML = '<p>Aucun compte.</p>';
                    selectedAccount.innerHTML = '<option value="">Aucun compte disponible</option>';
                    return;
                }

                const rows = accounts.map(acc => `
                    <tr>
                        <td>${acc.id}</td>
                        <td>${acc.holder}</td>
                        <td>${acc.email}</td>
                        <td>${acc.balance} €</td>
                        <td>${new Date(acc.created_at).toLocaleString()}</td>
                    </tr>
                `).join('');

                accountsEl.innerHTML = `
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nom</th>
                                <th>Email</th>
                                <th>Solde</th>
                                <th>Créé le</th>
                            </tr>
                        </thead>
                        <tbody>${rows}</tbody>
                    </table>
                `;

                selectedAccount.innerHTML = accounts.map(acc => `
                    <option value="${acc.id}">${acc.holder} — ${acc.balance} €</option>
                `).join('');
            } catch (error) {
                accountsEl.innerHTML = `<div class='message error'>Impossible de charger les comptes: ${error.message}</div>`;
            }
        }

        async function createAccount() {
            createMessage.innerHTML = '';
            const holder = document.getElementById('holder').value.trim();
            const email = document.getElementById('email').value.trim();
            if (!holder || !email) {
                createMessage.innerHTML = `<div class='message error'>Remplis le nom et l'email.</div>`;
                return;
            }
            try {
                const res = await fetch(`${apiBase}/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ holder, email })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || JSON.stringify(data));
                createMessage.innerHTML = `<div class='message success'>Compte créé: ${data.account.id}</div>`;
                document.getElementById('holder').value = '';
                document.getElementById('email').value = '';
                await loadAccounts();
            } catch (error) {
                createMessage.innerHTML = `<div class='message error'>Erreur: ${error.message}</div>`;
            }
        }

        async function operation(type) {
            operationMessage.innerHTML = '';
            const accountId = selectedAccount.value;
            const amount = parseFloat(document.getElementById('amount').value);
            if (!accountId) {
                operationMessage.innerHTML = `<div class='message error'>Sélectionne un compte.</div>`;
                return;
            }
            if (!amount || amount <= 0) {
                operationMessage.innerHTML = `<div class='message error'>Montant invalide.</div>`;
                return;
            }
            try {
                const res = await fetch(`${apiBase}/${accountId}/${type}/`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ amount })
                });
                const data = await res.json();
                if (!res.ok) throw new Error(data.error || JSON.stringify(data));
                operationMessage.innerHTML = `<div class='message success'>${data.message}</div>`;
                document.getElementById('amount').value = '';
                await loadAccounts();
            } catch (error) {
                operationMessage.innerHTML = `<div class='message error'>Erreur: ${error.message}</div>`;
            }
        }

        document.getElementById('refresh').addEventListener('click', loadAccounts);
        document.getElementById('createAccount').addEventListener('click', createAccount);
        document.getElementById('deposit').addEventListener('click', () => operation('deposit'));
        document.getElementById('withdraw').addEventListener('click', () => operation('withdraw'));

        showStatus();
        loadAccounts();
    </script>
</body>
</html>"""
        return HttpResponse(html, content_type='text/html')
