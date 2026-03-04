from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def cart_add(request, product_id):
    # must be POST (your form uses POST)
    if request.method != "POST":
        return redirect("product_list")

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    pid = str(product.id)

    cart[pid] = cart.get(pid, 0) + 1  # qty +1
    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart_detail")  # go to /cart/


def cart_detail(request):
    cart = request.session.get("cart", {})
    items = []
    grand_total = 0.0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=int(pid))
        qty = int(qty)
        total_price = float(product.price) * qty
        grand_total += total_price
        items.append({
            "product": product,
            "quantity": qty,
            "total_price": total_price
        })

    return render(request, "user/cart.html", {
        "cart_items": items,
        "grand_total": grand_total
    })


def cart_update(request, product_id, action):
    cart = request.session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        if action == "increment":
            cart[pid] += 1
        elif action == "decrement":
            if cart[pid] > 1:
                cart[pid] -= 1
            else:
                del cart[pid]
        
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart_detail")


def cart_remove(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]
        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart_detail")


def cart_clear(request):
    request.session["cart"] = {}
    request.session.modified = True
    return redirect("cart_detail")