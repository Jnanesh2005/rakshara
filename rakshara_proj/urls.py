from django.contrib import admin
from django.urls import path, include
from accounts.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('health/', include('health.urls')),
    path('classroom/', include('classroom.urls')),
    path('', home, name='home'),  # ✅ root/home view
]
