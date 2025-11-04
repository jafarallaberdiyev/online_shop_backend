
from decimal import Decimal
from catalog.models import Product

CART_SESSION_ID = 'cart'

class CartItem:
    def __init__(self, product, qty):
        self.product = product
        self.qty = qty

    @property
    def total(self):
        return self.product.price * self.qty

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, qty=1, update=False):
        product = Product.objects.get(id=product_id)
        pid = str(product_id)
        if pid not in self.cart:
            self.cart[pid] = {'qty': 0, 'price': str(product.price)}
        if update:
            self.cart[pid]['qty'] = qty
        else:
            self.cart[pid]['qty'] += qty
        self.save()

    def remove(self, product_id):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def save(self):
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    @property
    def items(self):
        ids = self.cart.keys()
        products = Product.objects.filter(id__in=ids)
        mapping = {str(p.id): p for p in products}
        return [CartItem(mapping[pid], data['qty']) for pid, data in self.cart.items() if pid in mapping]

    @property
    def total(self):
        from decimal import Decimal
        total = Decimal('0.00')
        for item in self.items:
            total += item.total
        return total
