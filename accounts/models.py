from django.db import models
from django.core.validators import MinValueValidator
import uuid

class Account(models.Model):
    """
    Modèle représentant un compte bancaire
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Identifiant unique du compte"
    )
    
    holder = models.CharField(
        max_length=255,
        verbose_name="Nom du titulaire"
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name="Adresse email"
    )
    
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00)],
        verbose_name="Solde du compte"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dernière modification"
    )

    class Meta:
        verbose_name = "Compte bancaire"
        verbose_name_plural = "Comptes bancaires"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.holder} - {self.email} ({self.balance} €)"
    
    # Méthode utilitaire pour les opérations
    def deposit(self, amount):
        """Déposer de l'argent sur le compte"""
        if amount <= 0:
            raise ValueError("Le montant du dépôt doit être positif")
        self.balance += amount
        self.save()
        return self.balance
    
    def withdraw(self, amount):
        """Retirer de l'argent du compte"""
        if amount <= 0:
            raise ValueError("Le montant du retrait doit être positif")
        if amount > self.balance:
            raise ValueError("Solde insuffisant")
        self.balance -= amount
        self.save()
        return self.balance