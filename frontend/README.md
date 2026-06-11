Client frontend léger pour l'API Banque

Comment lancer localement :

1. Ouvre un terminal dans `c:\Users\Pro\banque_api_django\frontend`
2. Démarre un serveur HTTP statique :

```bash
python -m http.server 8001
```

3. Ouvre un navigateur et va à : http://localhost:8001/

Notes :
- L'API doit être accessible à `http://localhost:8000/api/accounts/` (serveur Django en cours d'exécution).
- Le projet Django a déjà `CORS_ALLOW_ALL_ORIGINS = True` dans `banque_api/settings.py`, donc les appels fetch depuis ce frontend fonctionnent.
