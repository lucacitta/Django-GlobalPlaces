from rest_framework.viewsets import ReadOnlyModelViewSet

class ViewSetPermissionMixin:
    permissions = {
        "create": [],
        "list": [],
        "retrieve": [],
        "update": [],
        "partial_update": [],
        "destroy": [],
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, [])]


class ViewSetSerializerMixin:
    serializers = {
        "create": None,
        "list": None,
        "retrieve": None,
        "update": None,
        "partial_update": None,
        "destroy": None,
    }

    def get_serializer_class(self, *args, **kwargs):
        return self.serializers.get(self.action, None)

class BaseReadOnlyModelViewSet(
    ViewSetPermissionMixin,
    ViewSetSerializerMixin,
    ReadOnlyModelViewSet,
):
    pass

