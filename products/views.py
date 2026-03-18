from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import SellerRequestForm
from orders.models import OrderItem
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



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SellerRequestForm

@login_required
def become_seller(request):

    if request.method == "POST":
        form = SellerRequestForm(request.POST)

        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()

            return redirect("product_list")

    else:
        form = SellerRequestForm()

    return render(request,"seller/become_seller.html",{"form":form})


@login_required
def seller_dashboard(request):

    seller = SellerRequest.objects.filter(user=request.user, is_approved=True).first()

    if not seller:
        return redirect("become_seller")

    return render(request,"seller/dashboard.html")


from django.shortcuts import render, redirect
from .models import SellerRequest
from django.contrib.auth.decorators import login_required

@login_required
def seller_dashboard(request):

    try:
        seller = SellerRequest.objects.get(user=request.user)
    except SellerRequest.DoesNotExist:
        return redirect("become_seller")

    if not seller.approved:
        return redirect("become_seller")

    # Seller products
    products = Product.objects.filter(seller=request.user)

    # Seller orders (only orders containing seller's products)
    orders = OrderItem.objects.filter(product__seller=request.user).select_related("order", "product")

    # Calculate revenue
    total_revenue = 0
    for item in orders:
        total_revenue += item.price * item.qty

    context = {
        "product_count": products.count(),
        "order_count": orders.count(),
        "total_revenue": total_revenue,
        "recent_orders": orders.order_by("-order__created_at")[:5],
    }

    return render(request, "seller/dashboard.html", context)


from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Category, SellerRequest

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Category, SellerRequest


@login_required
def add_product(request):

    # only approved sellers can add products
    if not SellerRequest.objects.filter(user=request.user, approved=True).exists():
        return redirect("profile")

    categories = Category.objects.all()

    if request.method == "POST":

        name = request.POST.get("name")
        price = request.POST.get("price")
        stock = request.POST.get("stock")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")

        category = Category.objects.get(id=category_id) if category_id else None

        Product.objects.create(
            seller=request.user,
            category=category,
            name=name,
            price=price,
            stock=stock,
            description=description,
            image=image
        )

        return redirect("seller_dashboard")

    return render(request, "seller/add_product.html", {
        "categories": categories
    })


@login_required
def seller_products(request):

    products = Product.objects.filter(seller=request.user)

    return render(request, "seller/products.html", {
        "products": products
    })


from django.contrib.auth.decorators import login_required
from orders.models import OrderItem

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import OrderItem

@login_required
def seller_orders(request):

    orders = OrderItem.objects.filter(
        product__seller=request.user
    ).select_related("order", "product")

    total_revenue = 0

    for item in orders:
        item.total = item.price * item.qty
        total_revenue += item.total

    return render(request, "seller/orders.html", {
        "orders": orders,
        "total_revenue": total_revenue
    })