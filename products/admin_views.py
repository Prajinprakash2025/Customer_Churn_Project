from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category
from orders.models import Order
from django.db.models import Sum, F

@staff_member_required(login_url='/accounts/management-login/')
def admin_dashboard(request):
    from orders.models import OrderItem
    # Total revenue across all orders
    total_revenue = OrderItem.objects.aggregate(
        total=Sum(F('price') * F('qty'))
    )['total'] or 0
    
    # Recent orders with calculated total_price
    recent_orders = Order.objects.annotate(
        total_price=Sum(F('items__price') * F('items__qty'))
    ).order_by("-id")[:5]
    
    return render(request, "admin/dashboard.html", {
        "product_count": Product.objects.count(),
        "order_count": Order.objects.count(),
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
    })

@staff_member_required(login_url='/accounts/management-login/')
def admin_products(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "admin/products_list.html", {"products": products})

@staff_member_required(login_url='/accounts/management-login/')
def admin_product_add(request):
    categories = Category.objects.all()

    if request.method == "POST":
        image = request.FILES.get("image")

        Product.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
            description=request.POST.get("description", ""),
            category_id=request.POST.get("category") or None,
            image=image,
            is_active=True
        )
        messages.success(request, "Product added successfully.")
        return redirect("manage_products")

    return render(request, "admin/product_form.html", {
        "categories": categories,
        "mode": "add"
    })

@staff_member_required(login_url='/accounts/management-login/')
def admin_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.description = request.POST.get("description", "")
        product.category_id = request.POST.get("category") or None

        if request.FILES.get("image"):
            product.image = request.FILES.get("image")

        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect("manage_products")

    return render(request, "admin/product_form.html", {
        "product": product,
        "categories": categories,
        "mode": "edit"
    })

@staff_member_required(login_url='/accounts/management-login/')
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully.")
    return redirect("manage_products")

@staff_member_required(login_url='/accounts/management-login/')
def admin_orders(request):
    orders = Order.objects.annotate(
        total_price=Sum(F('items__price') * F('items__qty'))
    ).order_by("-id")
    return render(request, "admin/orders_list.html", {"orders": orders})

@staff_member_required(login_url='/accounts/management-login/')
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, "admin/category_list.html", {"categories": categories})

@staff_member_required(login_url='/accounts/management-login/')
def admin_category_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        icon = request.POST.get("icon")

        if name:
            Category.objects.create(name=name, icon=icon)
            messages.success(request, "Category added successfully.")
            return redirect("manage_categories")

    return render(request, "admin/category_form.html", {"mode": "add"})

@staff_member_required(login_url='/accounts/management-login/')
def admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.icon = request.POST.get("icon")
        category.save()
        messages.success(request, "Category updated successfully.")
        return redirect("manage_categories")

    return render(request, "admin/category_form.html", {"category": category, "mode": "edit"})

@staff_member_required(login_url='/accounts/management-login/')
def admin_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('manage_categories')
    return render(request, 'admin/category_confirm_delete.html', {'category': category})

@staff_member_required(login_url='/accounts/management-login/')
def admin_bulk_delete_products(request):
    if request.method == "POST":
        product_ids = request.POST.getlist('product_ids')
        if product_ids:
            Product.objects.filter(id__in=product_ids).delete()
            messages.success(request, f"Successfully deleted {len(product_ids)} products.")
        else:
            messages.warning(request, "No products selected.")
    return redirect("manage_products")

@staff_member_required(login_url='/accounts/management-login/')
def admin_bulk_delete_categories(request):
    if request.method == "POST":
        category_ids = request.POST.getlist('category_ids')
        if category_ids:
            Category.objects.filter(id__in=category_ids).delete()
            messages.success(request, f"Successfully deleted {len(category_ids)} categories.")
        else:
            messages.warning(request, "No categories selected.")
    return redirect("manage_categories")