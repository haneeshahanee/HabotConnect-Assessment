from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include

def home(request):
    return JsonResponse({
        "message": "Employee Management API is running"
    })

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include('employees.urls')),
]
