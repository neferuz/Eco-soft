from django.contrib import admin
from django.urls import path, include
from . import views
from .views import birutti_menu_api, products_api, product_detail_api
import nested_admin

urlpatterns = [
    path('', views.index, name='index'),
    path('logo/', views.site_logo_api, name='site_logo_api'),
    path('categories/', views.get_categories, name='categories'),
    path('menu/', views.get_menu_structure, name='menu_structure'),
    path('product-lines/', views.get_product_lines, name='get_product_lines'),
    path('cards/', views.cards_api, name='cards_api'),
    path('menu-categories/', views.menu_categories_api, name='menu_categories_api'),
    path('brands-block/', views.brands_block_api, name='brands_block_api'),
    path('gender-banners/', views.gender_banners_api, name='gender_banners_api'),
    path('carousel/', views.carousel_api, name='carousel_api'),
    path('landing-video-block/', views.landing_video_block_api, name='landing_video_block_api'),
    path('contact/', views.contacts, name='contacts'),
    path('contacts/', views.contacts, name='contacts'),
    path('about.html', views.about_html, name='about_html'),
    path('shop.html', views.shop_view, name='shop'),
    path('site-logo/', views.site_logo_api, name='site-logo'),
    path('about/', views.about_html, name='about'),
    path('api/about/', views.get_about_data, name='about-data'),
    path('api/category/<int:category_id>/subcategories/', views.get_category_subcategories, name='category-subcategories'),
    path('api/birutti-menu/', birutti_menu_api, name='birutti-menu-api'),
    path('shop-menu/', views.shop_menu_api, name='shop-menu-api'),
    path('api/products/', products_api, name='products_api'),
    path('api/product/<int:pk>/', product_detail_api, name='product_detail_api'),
    path('product.html', views.product_html, name='product_html'),
    path('shop/product.html', views.product_html, name='product_html_shop'),
    path('nested_admin/', include('nested_admin.urls')),
    path('admin/', admin.site.urls),
    path('shop/product/<int:id>/', views.product_detail, name='product_detail'),
    path('category-products/', views.category_products_view, name='category_products'),
]