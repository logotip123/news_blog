from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from blog.models import Post, Comment
from .models import CustomUser


def populate_models(sender, **kwargs):
    admins, _ = Group.objects.get_or_create(name="Administrators")
    redactors, _ = Group.objects.get_or_create(name="Redactors")
    users, _ = Group.objects.get_or_create(name="Users")

    content_type = ContentType.objects.get_for_model(Post)
    add, change, delete, view = Permission.objects.filter(content_type=content_type).all()
    admins.permissions.add(add, change, delete, view)
    redactors.permissions.add(add, change, view)
    users.permissions.add(add, view)

    content_type = ContentType.objects.get_for_model(Comment)
    add, change, delete, view = Permission.objects.filter(content_type=content_type).all()
    admins.permissions.add(delete, change, view)
    redactors.permissions.add(delete, change, view)

    content_type = ContentType.objects.get_for_model(CustomUser)
    add, change, delete, view = Permission.objects.filter(content_type=content_type).all()
    admins.permissions.add(add, delete, change, view)