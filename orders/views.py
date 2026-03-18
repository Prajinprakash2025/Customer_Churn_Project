from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem,Address
from .models import *
from products.models import Product

def _get_cart(session):
    return session.get("cart", {})

@login_required
def checkout(request):

    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart_detail")

    cart_items = []
    grand_total = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=int(pid))

        total_price = product.price * int(qty)

        cart_items.append({
            "product": product,
            "qty": qty,
            "total_price": total_price
        })

        grand_total += total_price

    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":

        address_id = request.POST.get("address_id")

        # Existing address
        if address_id:
            selected_address = get_object_or_404(Address, id=address_id, user=request.user)

            full_name = selected_address.full_name
            phone = selected_address.phone
            address_text = f"{selected_address.address_line}, {selected_address.city}, {selected_address.state} - {selected_address.pincode}"

        else:
            # New address
            full_name = request.POST.get("full_name")
            phone = request.POST.get("phone")
            address_text = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address_text
        )

        for pid, qty in cart.items():

            product = get_object_or_404(Product, pk=int(pid))

            OrderItem.objects.create(
                order=order,
                product=product,
                qty=int(qty),
                price=product.price
            )

            product.stock -= int(qty)
            product.save()

        request.session.pop("cart", None)

        return redirect("order_success", order_id=order.id)

    return render(request, "user/checkout.html", {
        "addresses": addresses,
        "cart_items": cart_items,
        "grand_total": grand_total
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "user/order_success.html", {"order": order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    return render(request, "user/my_orders.html", {"orders": orders})