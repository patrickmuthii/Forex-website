from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

# Currency Model
class Currency(models.Model):
    code = models.CharField(max_length=5, unique=True)  # e.g. USD, EUR
    name = models.CharField(max_length=50)  # e.g. US Dollar

    def __str__(self):
        return f"{self.code} - {self.name}"


# Forex Pair Model
class ForexPair(models.Model):
    base_currency = models.ForeignKey(Currency, related_name='base_pairs', on_delete=models.CASCADE)
    quote_currency = models.ForeignKey(Currency, related_name='quote_pairs', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, unique=True)  # e.g. EURUSD

    def __str__(self):
        return f"{self.base_currency.code}/{self.quote_currency.code}"


# Price History Model
class PriceHistory(models.Model):
    pair = models.ForeignKey(ForexPair, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_digits=10, decimal_places=5)
    high_price = models.DecimalField(max_digits=10, decimal_places=5)
    low_price = models.DecimalField(max_digits=10, decimal_places=5)
    close_price = models.DecimalField(max_digits=10, decimal_places=5)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ('pair', 'timestamp')

    def __str__(self):
        return f"{self.pair.symbol} - {self.timestamp}"


# Trade Model
class Trade(models.Model):
    TRADE_TYPE_CHOICES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pair = models.ForeignKey(ForexPair, on_delete=models.CASCADE)
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPE_CHOICES)
    entry_price = models.DecimalField(max_digits=10, decimal_places=5)
    exit_price = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    take_profit = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.pair.symbol} ({self.trade_type})"


# Watchlist Model
class Watchlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pair = models.ForeignKey(ForexPair, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pair')

    def __str__(self):
        return f"{self.user.username} - {self.pair.symbol}"

# Create your models here.

