# from django.contrib import admin
# from django.urls import path,include
# from django.conf import settings

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('API.urls')),
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.http import JsonResponse
from django.views.static import serve

def root(request):
    return JsonResponse({"message": "Food Ordering API is running!", "status": "ok"})

urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path('', include('API.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
