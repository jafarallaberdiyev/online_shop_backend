from django.urls import path
from . import views
app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

]
