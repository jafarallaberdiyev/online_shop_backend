from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from orders import views as order_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls', namespace='catalog')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('stripe/success/', order_views.stripe_success, name='stripe_success'),
    path('stripe/cancel/',  order_views.stripe_cancel,  name='stripe_cancel'),
    path('stripe/webhook/', order_views.stripe_webhook, name='stripe_webhook'),

]

info_patterns = ([
    path('about/', TemplateView.as_view(template_name='info/about.html'), name='about'),
    path('shipping-payment/', TemplateView.as_view(template_name='info/shipping_payment.html'), name='shipping_payment'),
    path('contacts/', TemplateView.as_view(template_name='info/contacts.html'), name='contacts'),
], 'info')

urlpatterns += [
    path('info/', include(info_patterns, namespace='info')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)