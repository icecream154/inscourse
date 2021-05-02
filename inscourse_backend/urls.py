from django.urls import path

from inscourse_backend.services.sys.users import login, change_username

urlpatterns = [
    path('sys/login', login, name='login'),
    path('sys/changeName', change_username, name='change_username')
]