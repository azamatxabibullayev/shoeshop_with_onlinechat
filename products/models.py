from django.contrib.auth.models import User
from django.db import models
from users.models import Painting
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class CategoryProducts(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'category_products'

    def __str__(self):
        return self.name


class TypeProduct(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'type_product'

    def __str__(self):
        return self.name


class SizeProduct(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'size_product'

    def __str__(self):
        return self.name


class ColorProduct(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'color_product'

    def __str__(self):
        return self.name


class MadeCompany(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'made_company'

    def __str__(self):
        return self.name


class MadeCountry(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'made_country'

    def __str__(self):
        return self.name


class Lather(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'lather'

    def __str__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'season'

    def __str__(self):
        return self.name


class Shoes(models.Model):
    category = models.ForeignKey(CategoryProducts, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products_image/', blank=True, null=True)
    price = models.IntegerField()
    type = models.ForeignKey(TypeProduct, on_delete=models.CASCADE)
    size = models.ForeignKey(SizeProduct, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorProduct, on_delete=models.CASCADE)
    made_company = models.ForeignKey(MadeCompany, on_delete=models.CASCADE)
    made_country = models.ForeignKey(MadeCountry, on_delete=models.CASCADE)
    lather = models.ForeignKey(Lather, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"Review by {self.user.username} for {self.shoe}"
