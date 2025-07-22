from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('credit_app.urls')),  # 👈 This must include 'credit_app'
]
