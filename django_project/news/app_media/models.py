from django.db import models


class Goods(models.Model):
    vendor_code = models.CharField(max_length=20, verbose_name='Vendor code')
    quantity = models.IntegerField(verbose_name='Quantity')
    price = models.IntegerField(verbose_name='Price')

    @property
    def costs(self):
        return self.price * self.quantity


class File(models.Model):
    file = models.FileField(upload_to='files/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
