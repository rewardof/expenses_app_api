from rest_framework import permissions


class IsCurrentUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if obj.user == request.user:
            return True


class IsOwnerUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
        #     return True
        if obj.profile.user == request.user:
            return True
