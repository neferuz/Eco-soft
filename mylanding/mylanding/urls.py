from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from content import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop_view, name='shop'),
    path('about/', views.about_html, name='about'),
    path('category-products/', views.category_products_view, name='category_products'),
    path('product/', views.product_view, name='product'),
    path('women/', views.women_view, name='women'),
    path('kids/', views.kids_view, name='kids'),
    path('contacts.html', views.contacts, name='contacts'),
    path('admin/', admin.site.urls),
    path('api/', include('content.urls')),
    path('', include('content.urls')),
    # path('nested_admin/', include('nested_admin.urls')),
    
]


schema_view = get_schema_view(
    openapi.Info(
        title="EcoSoft API",
        default_version='v1',
        description="Документация всех API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
