from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urls = [
    path('products/', include('base.urls.product_urls')),
    path('users/', include('base.urls.user_urls')),
    path('orders/', include('base.urls.order_urls')),
    path('air/', include('base.urls.air_urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urls)),
    path('', TemplateView.as_view(template_name='index.html'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
