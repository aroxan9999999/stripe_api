from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    img = models.ImageField(upload_to=f'product/')

    def __str__(self):
        return self.name

    def get_price(self):
        return "{0:.2f}".format(self.price / 100)

    def get_discount_price(self):
        discount = Discount.objects.get(pk=self.pk)
        if discount:
            return '{0:.2f}'.format((self.price * discount) // 100)


class Order(models.Model):
    products = models.ManyToManyField(Item)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(user, on_delete=models.PROTECT)
    many = models.BooleanField(default=False, editable=False)
    item_pk = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return ' '.join([p.name for p in self.products.all()])

    def get_price(self):
        return '{0:.2f}'.format(
            sum([float(d_price.get_price()) for d_price in
                 self.products.all()]+[0]))

    def get_cent_price(self):
        sum([d_price.price for d_price in self.products.all()] + [0])



class Discount(models.Model):
    discount = models.ForeignKey(Item, on_delete=models.CASCADE)
    procent = models.IntegerField(default=0)

    def __str__(self):
        return self.procent


class Currency(models.Model):
    currency = models.CharField(max_length=3, default='usd', unique=True)

    def __str__(self):
        return self.currency


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
