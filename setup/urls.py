from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'), 
    path('', include('apps.dashboard.urls')),
    path('financeiro/', include('apps.financeiro.urls')),
    path('rh/', include('apps.recursos_humanos.urls')),
    path('vendas/', include('apps.vendas.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)