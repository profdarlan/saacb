from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.views.decorators.cache import never_cache


@never_cache
def admin_login(request):
    return render(request, 'admin_login.html')

urlpatterns = [
    path('', RedirectView.as_view(url='/tarefas/'), name='home'),
    path('admin/', admin.site.urls),
    path('tarefas/', include('tarefas.urls')),
    path('gru/', include('tarefas.gru.urls')),

]

# Servir static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Sempre servir arquivos media (DEBUG ou não)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)