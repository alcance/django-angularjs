from rest_framework import permissions


# Check whether that user is the same objects as account.
# If no user associated with this request return False
class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user

        return False
