from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Cart, CartItem, Product, Order, OrderItem

def ensure_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        sk = ensure_session_key(request)
        cart, _ = Cart.objects.get_or_create(session_key=sk, user=None)
    return cart

def merge_guest_cart_to_user(request, user):
    """Fusiona el carrito de sesión (si existe) al del usuario."""
    sk = request.session.session_key
    if not sk:
        return
    try:
        guest_cart = Cart.objects.get(session_key=sk, user=None)
    except Cart.DoesNotExist:
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)
    # fusiona items
    for gi in guest_cart.items.all():
        ui, created = user_cart.items.get_or_create(
            product=gi.product,
            defaults={"qty": gi.qty, "unit_price": gi.unit_price}
        )
        if not created:
            ui.qty += gi.qty
            ui.save(update_fields=["qty"])
    guest_cart.delete()

def compute_shipping(cart) -> Decimal:
    # Regla simple: envío fijo si hay items
    return Decimal("0.00") if cart.items.count() == 0 else Decimal("4.990")

def next_order_number() -> str:
    today = timezone.now().strftime("%Y%m%d")
    prefix = f"ORD-{today}-"
    last = Order.objects.filter(number__startswith=prefix).order_by("-number").first()
    seq = 1
    if last:
        try:
            seq = int(last.number.split("-")[-1]) + 1
        except Exception:
            seq = 1
    return f"{prefix}{seq:04d}"

@transaction.atomic
def create_order_from_cart(request, payload: dict) -> Order:
    """
    Crea Order + OrderItems desde el carrito actual.
    Valida stock, descuenta inventario y vacía el carrito.
    """
    cart = get_or_create_cart(request)
    items = list(cart.items.select_related("product"))
    if not items:
        raise ValueError("empty_cart")

    # Validar stock
    for it in items:
        if it.qty > it.product.stock:
            raise ValueError(f"no_stock:{it.product.id}")

    # Calcular totales
    subtotal = sum((it.subtotal for it in items), Decimal("0.00"))
    shipping = compute_shipping(cart)
    total = subtotal + shipping

    # Crear orden
    o = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        email=payload.get("email"),
        full_name=payload.get("full_name"),
        phone=payload.get("phone",""),
        address=payload.get("address"),
        city=payload.get("city"),
        region=payload.get("region",""),
        notes=payload.get("notes",""),
        subtotal=subtotal,
        shipping=shipping,
        total=total,
        number=next_order_number(),
        status="pending",
    )

    # Items + descuento de stock
    for it in items:
        OrderItem.objects.create(
            order=o,
            product=it.product,
            qty=it.qty,
            unit_price=it.unit_price,
            subtotal=it.subtotal
        )
        it.product.stock -= it.qty
        it.product.save(update_fields=["stock"])

    # Vaciar carrito
    cart.items.all().delete()
    return o