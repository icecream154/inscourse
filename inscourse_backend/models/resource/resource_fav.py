from django.db import models

from inscourse_backend.models.resource.resource import Resource
from inscourse_backend.models.user import User


class ResourceFav(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
