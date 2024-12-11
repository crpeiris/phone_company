from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom user manager to handle staff user creation
class StaffUserManager(BaseUserManager):
    def create_user(self, username, email, telephone, password=None):
        if not username:
            raise ValueError(_('The Username must be set'))
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            telephone=telephone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, telephone, password=None):
        user = self.create_user(
            username=username,
            email=email,
            telephone=telephone,
            password=password
        )
        user.is_staff = True  # Mark as staff member
        user.save(using=self._db)
        return user

# Custom user model for staff
class Staff(AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    telephone = models.CharField(_('telephone number'), max_length=15, blank=True, null=True)

    objects = StaffUserManager()

    class Meta:
        verbose_name = _('Staff')
        verbose_name_plural = _('Staff')

    def __str__(self):
        return self.username

    # Override the related_name to avoid conflicts
    groups = models.ManyToManyField(Group, related_name='staff_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='staff_user_permissions', blank=True)


# Role model for different staff roles
class Role(models.Model):
    name = models.CharField(_('role name'), max_length=50, unique=True)
    permissions = models.ManyToManyField('auth.Permission', related_name='roles', blank=True)

    def __str__(self):
        return self.name

# Order model for managing orders
class Order(models.Model):
    status = models.CharField(_('order status'), max_length=20)
    pay_reference = models.CharField(_('payment reference'), max_length=50, blank=True, null=True)
    delivery_reference = models.CharField(_('delivery reference'), max_length=50, blank=True, null=True)
    customer = models.CharField(_('customer'), max_length=100)
    date = models.DateTimeField(_('date'), auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.status}'

# Product model for managing products
class Product(models.Model):
    name = models.CharField(_('product name'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
