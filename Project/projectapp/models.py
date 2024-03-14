from django.db import models


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)  # Added slug field
    image = models.ImageField(upload_to='category_images', blank=True, null=True)  # Added image field

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Cart(models.Model):
    objects = None
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)