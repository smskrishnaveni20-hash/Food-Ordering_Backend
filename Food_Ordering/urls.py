from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import staticfrom django.http import JsonResponse

def root(request):
    return JsonResponse({"message": "Food Ordering API is running!", "status": "ok"})


urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path('', include('API.urls')),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
