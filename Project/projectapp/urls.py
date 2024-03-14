from django.urls import path
from .views import (index_page, category_detail, product_detail, add_to_cart, view_cart,
                    update_cart, delete_cart_item, search_view)
urlpatterns = [
    path('', index_page, name='index_page'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('view-cart/', view_cart, name='view_cart'),
    path('update/<int:cart_item_id>/', update_cart, name='update_cart'),
    path('delete/<int:cart_item_id>/', delete_cart_item, name='delete_cart_item'),
    path('search/',search_view, name='search'),

    # path('add/', admin_panel, name='admin_panel'),
    # path('add_category/', add_category, name='add_category'),
]