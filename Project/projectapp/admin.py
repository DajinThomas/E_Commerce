from django.contrib import admin
from .models import Category, Product, Cart


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'created_at', 'updated_at']  # Updated field names
    search_fields = ['name', 'category__name']
    list_filter = ['category']
    list_per_page = 29  # Set the number of items per page


admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'slug', 'image']  # Updated field names
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_filter = ['name']
    list_per_page = 29  # Set the number of items per page


admin.site.register(Category, CategoryAdmin)

admin.site.register(Cart)