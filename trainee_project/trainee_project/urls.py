from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('repository.urls')),
    path('api/repository/', include('repository.apiurls')),
    path('api/auth/', include('account.apiurls'))
]
