from django.db import models

# Create your models here.

class WooCommerce(models.Model):
    id_order = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.id_order
    
    
class SecretKey(models.Model):
    terminal_code = models.CharField(max_length=255)
    secret_key = models.CharField(max_length=255)