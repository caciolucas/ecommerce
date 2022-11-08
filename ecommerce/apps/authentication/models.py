from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    PermissionsMixin as BasicPermissions,
    UserManager as BaseUserManager,
)

from commerce.models import Cart
from common.models import AutoTimestampedModel, UUIDModel


# Create your models here.


class Permission(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    codename = models.CharField(_("Codename"), max_length=100, unique=True)

    class Meta:
        verbose_name = _("Permission")
        verbose_name_plural = _("Permissions")

    def __str__(self):
        return "%s" % self.name


class Group(models.Model):
    name = models.CharField(_("Name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission, verbose_name=_("Permissions"), blank=True
    )

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return self.name


class PermissionsMixin(BasicPermissions):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, username, email, name, password):
        if not username:
            raise ValueError("Please provide an username")
        if not email:
            raise ValueError("Please provide an email")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        # Create empty cart for user
        Cart.objects.create(user=user)
        return user

    def create_superuser(self, username, email, name, password, **extra_fields):
        user = self.create_user(username, email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin, AutoTimestampedModel, UUIDModel):
    name = models.CharField(_("Name"), max_length=255)
    username = models.CharField(_("Username"), max_length=255, unique=True)
    email = models.EmailField(_("Email"))
    profile_picture = models.FileField(_("Profile Picture"), null=True)
    is_staff = models.BooleanField(
        _("Is Staff"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Profile Picture"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "name"]

    objects = UserManager()

    class Meta:
        app_label = "authentication"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.name} @{self.username}"
