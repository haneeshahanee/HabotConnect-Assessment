from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, register_user, login_user

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
]
