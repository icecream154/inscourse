from inscourse_backend.models.resource.resource import Resource
from inscourse_backend.models.resource.resource_fav import ResourceFav
from inscourse_backend.models.resource.resource_prefer import ResourcePrefer
from inscourse_backend.models.user import User


def to_resource_dict(resource: Resource, user: User):
    dic = resource.to_dict()
    dic['is_favored'] = ResourceFav.objects.filter(resource=resource, user=user).exists()
    dic['is_preferred'] = ResourcePrefer.objects.filter(resource=resource, user=user).exists()
    return dic
