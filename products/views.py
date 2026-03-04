from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Product, Wishlist, Category, Banner


def product_list(request):
    products = Product.objects.filter(is_active=True).order_by("-id")
    categories = Category.objects.all()
    banners = Banner.objects.filter(is_active=True).order_by('order')

    wishlist_products = []
    if request.user.is_authenticated:
        wishlist_products = Wishlist.objects.filter(
            user=request.user
        ).values_list("product_id", flat=True)

    return render(request, "user/product_list.html", {
        "products": products,
        "categories": categories,
        "banners": banners,
        "wishlist_products": wishlist_products,
    })



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, "user/product_detail.html", {"product": product})


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product,
    )

    return redirect("wishlist_detail")


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.filter(
        user=request.user,
        product=product,
    ).delete()

    return redirect("wishlist_detail")


@login_required
def wishlist_detail(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related("product")
    return render(request, "user/wishlist.html", {
        "wishlist_items": wishlist_items,
    })


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category, is_active=True)

    return render(request, "user/category_products.html", {
        "category": category,
        "products": products,
    })


def search_products(request):
    query = (request.GET.get("q") or "").strip()
    category_id = request.GET.get("category")

    products = Product.objects.filter(is_active=True)

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    if category_id and category_id != "all":
        products = products.filter(category_id=category_id)

    context = {
        "products": products.order_by("-id"),
        "query": query,
    }

    return render(request, "user/search_results.html", context)