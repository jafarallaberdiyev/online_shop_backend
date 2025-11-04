from .models import Product, Category
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

def index(request):
    qs = Product.objects.filter(is_active=True, stock__gt=0).select_related("category")
    featured = qs.order_by("-id")[:8]
    categories = Category.objects.all()
    return render(request, 'index.html', {'featured': featured, 'categories': categories})

def catalog_view(request):
    qs = Product.objects.filter(is_active=True)

    cat_slug = request.GET.get('category')
    current_category = None
    if cat_slug:
        current_category = get_object_or_404(Category, slug=cat_slug)
        qs = qs.filter(category__slug=cat_slug)

    if request.GET.get('on_sale'):
        qs = qs.exclude(old_price__isnull=True)

    q = request.GET.get('q')
    if q:
        qs = qs.filter(title__icontains=q)

    # ORDERING
    order_by = request.GET.get('order_by', 'default')
    if order_by == 'price':
        qs = qs.order_by('price')
    elif order_by == '-price':
        qs = qs.order_by('-price')
    else:
        qs = qs.order_by('-created_at')

    if request.GET.get("show") != "all":
        qs = qs.filter(stock__gt=0)

    paginator = Paginator(qs, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    categories = Category.objects.all()
    return render(
        request,
        'goods/catalog.html',
        {
            'page_obj': page_obj,
            'categories': categories,
            'current_category': current_category,
        },
    )

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    categories = Category.objects.all()
    return render(request, 'goods/product.html', {'product': product, 'categories': categories})
