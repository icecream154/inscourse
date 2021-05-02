from django.contrib import admin

# Register your models here.
from inscourse_backend.models.user import User

admin.site.register(User)