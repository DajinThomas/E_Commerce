from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Category, Product, Cart
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index_page(request):
    categories_list = Category.objects.all()
    total_items_in_cart = 0  # Default value in case user is not authenticated

    paginator = Paginator(categories_list, 4)  # Show 4 categories per page

    page_number = request.GET.get('page', 1)
    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        categories = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)  # If page is out of range (e.g. 9999), deliver last page of results.

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Query the Cart model for the total quantity of items for the authenticated user
        total_items_in_cart = Cart.objects.filter(user=request.user).aggregate(total_quantity=Sum('quantity'))['total_quantity']

        if total_items_in_cart is None:
            total_items_in_cart = 0

    return render(request, 'index.html', {'categories': categories, 'total_items_in_cart': total_items_in_cart})


def category_detail(request, slug):
    category_list = Category.objects.all()
    category = get_object_or_404(Category, slug=slug)
    products_list = Product.objects.filter(category=category)

    paginator = Paginator(products_list, 4)  # Show 4 categories per page

    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  # If page is out of range (e.g. 9999), deliver last page of results.

    # Assuming you have a 'category_detail.html' template
    return render(request, 'category_detail.html', {'category': category, 'category_list': category_list, 'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user if request.user.is_authenticated else None

    # Check if the product already exists in the user's cart
    existing_cart_item = Cart.objects.filter(product=product, user=user).first()

    if existing_cart_item:
        # If the product exists, update the quantity
        existing_cart_item.quantity += 1
        existing_cart_item.save()
    else:
        # If the product doesn't exist, create a new cart item
        cart_item = Cart.objects.create(
            product=product,
            user=user,
            quantity=1,
            price=product.price
        )

    return redirect('view_cart')


def view_cart(request):
    cart_items_list = Cart.objects.filter(user=request.user if request.user.is_authenticated else None)
    cart_items_Total = Cart.objects.filter(user=request.user if request.user.is_authenticated else None)
    paginator = Paginator(cart_items_list, 2)  # Show 4 categories per page

    page_number = request.GET.get('page', 1)
    try:
        cart_items = paginator.page(page_number)
    except PageNotAnInteger:
        cart_items = paginator.page(1)  # If page is not an integer, deliver first page.
    except EmptyPage:
        cart_items = paginator.page(
            paginator.num_pages)  # If page is out of range (e.g. 9999), deliver last page of results.

    total_price = sum(item.price for item in cart_items_Total)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    new_quantity = int(request.POST.get('quantity'))
    old_quantity = cart_item.quantity
    cart_item.quantity = new_quantity
    cart_item.price = cart_item.product.price * new_quantity
    cart_item.save()
    return redirect('view_cart')


def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(Cart, pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


def search_view(request):
    query = request.GET.get('query')
    results = None

    if query:
        # Perform search query on Product name and description fields
        results = Product.objects.filter(name__icontains=query) | Product.objects.filter(description__icontains=query)

    return render(request, 'search_results.html', {'results': results, 'query': query})


# # Action Panel
#
# from .models import Category
# from .forms import CategoryForm


# def admin_panel (request):
#     return render(request, 'Admin_Panel.html')


# def add_category(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('/')  # Redirect to category list page
#     else:
#         form = CategoryForm()
#     return render(request, 'add_category.html', {'form': form})
#
#
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Category
# from .forms import CategoryForm
#
#
# def edit_category(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, request.FILES, instance=category)
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#     else:
#         form = CategoryForm(instance=category)
#     return render(request, 'edit_category.html', {'form': form, 'category': category})