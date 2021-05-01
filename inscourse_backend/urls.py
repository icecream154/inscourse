from django.urls import path

from inscourse_backend.services.sys.users import login

urlpatterns = [
    path('sys/login', login, name='login')
]