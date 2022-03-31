from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=16)
    num = models.CharField(max_length=12, unique=True)
    role = models.CharField(max_length=1, blank=False, null=False)

    # driver = models.OneToOneField('DriverAcc', on_delete=models.CASCADE, null=True, blank=True)
    # company = models.OneToOneField('CompanyAcc', on_delete=models.CASCADE, null=True, blank=True)

    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def is_staff(self):
        return self.is_admin
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return self.is_admin
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'kingbus_user'

    def __str__(self):
        return self.username