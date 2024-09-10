from rest_framework import permissions


class IsAuthenticatedAuthor(permissions.IsAuthenticated):
    """
    Object-level permission to only allow authors of a post to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user
