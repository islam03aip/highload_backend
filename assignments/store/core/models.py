from django.db import models, transaction
from django.core.cache import cache
from celery import shared_task

class Item(models.Model):
    key = models.CharField(max_length=255, unique=True) # key
    name = models.CharField(max_length=70) # value
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def update_price(self, new_price):
        with transaction.atomic():
            self.price = new_price
            self.save()

    def update_price_async(self, new_price):
        self.price = new_price
        self.save()

        propagate_price_update.delay(self.id, new_price)

    def update_price_causally(self, new_price, timestamp):
        if timestamp > self.last_updated:
            self.price = new_price
            self.last_updated = timestamp
            self.save()

@shared_task
def propagate_price_update(product_id, new_price):
    product = Item.objects.get(id=product_id)
    product.price = new_price
    product.save()
    cache.set(f'product_price_{product_id}', new_price)  # Cache the new price