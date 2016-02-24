from django.db import models


class TimeStampedModel (models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Payee (TimeStampedModel):
    name = models.TextField()

    def __str__(self):
        return self.name


class ProductCategory (models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Product (TimeStampedModel):
    name = models.TextField()
    slug = models.CharField(max_length=64)
    price = models.PositiveIntegerField(null=True, blank=True)
    summary = models.TextField()
    description = models.TextField()
    categories = models.ManyToManyField('ProductCategory')
    department = models.ManyToManyField('Payee')

    def __str__(self):
        return self.name


class Invoice (TimeStampedModel):
    payee = models.ForeignKey('Payee', null=True)
    # product = models.ForeignKey('Product', null=True)
    invoicee = models.CharField('The ID of the entity being invoiced', max_length=32, blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    summary = models.TextField()
    data = models.TextField(default='{}')
    callback = models.URLField(null=True, blank=True)
    redirect = models.URLField(null=True, blank=True)

    def __str__(self):
        return '{} (${})'.format(self.summary, self.amount)


class Transaction (TimeStampedModel):
    invoice = models.ForeignKey('Invoice')
    amount = models.DecimalField(decimal_places=2, max_digits=12)      # Note that this can be negative, in the case of refunds
    timestamp = models.DateTimeField()
    external_id = models.TextField()    # Upstream payment ID
    external_data = models.TextField()  # The data, verbatim, from upstream

    def __str__(self):
        return '{} ({}) - ${}'.format(
            self.invoice, self.merch_key, self.amount)