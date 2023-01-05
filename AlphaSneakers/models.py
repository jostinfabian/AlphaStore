from django.db import models

# Create your models here.
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class Brand(models.Model):
    name = models.CharField(max_length=50)


class Sneaker(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=5)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)


class SneakerImage(models.Model):
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sneaker_images')


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    shipping_address = models.CharField(max_length=200)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    shipping_name = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=200)
    shipping_zip_code = models.CharField(max_length=10)


class BillingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    card_holder_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=20)
    expiration_date = models.DateField()


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=10, decimal_places=2)


class Promotion(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    discount = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class SocialPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)


def __str__(self):
    return self.title
