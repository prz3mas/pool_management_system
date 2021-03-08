from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('manage/', include('management_systems.urls')),
    path('', lambda req: redirect('/manage/home/'))
]
