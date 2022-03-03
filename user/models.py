import os
from uuid import uuid4
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from community.models import Profile
# below imports are for global services localizations
# from django.utils import timezone 
# from django.utils.translation import ugettext_lazy as _


# https://gumdrop.tistory.com/23
class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', False)
        # extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_admin', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        return self._create_user(username, email, password, **extra_fields)


def upload_to_func_common(instance, filename):
    prefix = timezone.now().strftime("%Y/%m/%d")
    file_name = uuid4().hex
    extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
    return "/".join([prefix, file_name+extension])


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

    objects = UserManager()

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




class DriverAcc(models.Model):
    def upload_to_func_driver_car_driverlicense(instance, filename):
        return "/".join(['driver_car_driverlicense',upload_to_func_common(instance, filename)])
    def upload_to_func_driver_car_photo(instance, filename):
        return "/".join(['driver_car_photo',upload_to_func_common(instance, filename)])
    def upload_to_func_driver_profile_tradeunion_certificate(instance, filename):
        return "/".join(['driver_profile_tradeunion_certificate',upload_to_func_common(instance, filename)])
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # username = models.CharField(max_length=32, unique=True)
    # email = models.EmailField(max_length=255, unique=True)
    # name = models.CharField(max_length=16)
    # num = models.CharField(max_length=12, unique=True)
    driver_com_name = models.CharField(max_length=32)
    driver_car_driverlicense = models.ImageField(upload_to=upload_to_func_driver_car_driverlicense)
    # Profile section below
    driver_car_option = models.CharField(max_length=128, null=True, blank=True)
    driver_car_num = models.CharField(max_length=10, null=True, blank=True)
    driver_car_kind = models.CharField(max_length=32, null=True, blank=True)
    driver_car_year = models.CharField(max_length=4, null=True, blank=True)
    driver_car_photo = models.ImageField(upload_to=upload_to_func_driver_car_photo, null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    driver_profile_tradeunion_certificate = models.FileField(upload_to=upload_to_func_driver_profile_tradeunion_certificate, null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    driver_profile_introduction = models.CharField(max_length=200, null=True, blank=True)
    driver_profile_introduction_video = models.TextField(null=True, blank=True)
    #models.FileField(upload_to="driver_introduction_video"+str(upload_to_func_common), null=True, blank=True) # TODO Youtube or File upload
    driver_profile_location = models.CharField(max_length=128, null=True, blank=True)

    # is_admin = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    # created_on = models.DateTimeField(auto_now_add=True)
    # updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kingbus_driver_profile'
    def __str__(self):
        return str(self.user)

    # objects = UserManager()

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['userid']
    filesavefield = 'driveracc'




class CompanyAcc(models.Model):
    def upload_to_func_company_business_registration(instance, filename):
        return "/".join(['company_business_registration',upload_to_func_common(instance, filename)])
    def upload_to_func_company_profile_transportationbusiness_registration(instance, filename):
        return "/".join(['company_profile_transportationbusiness_registration',upload_to_func_common(instance, filename)])
    def upload_to_func_company_profile_tradeunion_certificate(instance, filename):
        return "/".join(['company_profile_tradeunion_certificate',upload_to_func_common(instance, filename)])
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # username = models.CharField(max_length=32, unique=True)
    # email = models.EmailField(max_length=255, unique=True)# manager's email
    # name = models.CharField(max_length=16)# manager's name
    # num = models.CharField(max_length=12, unique=True)
    company_com_name = models.CharField(max_length=32)
    company_business_registration = models.ImageField(upload_to=upload_to_func_company_business_registration)
    # Profile section below
    company_profile_transportationbusiness_registration = models.ImageField(upload_to=upload_to_func_company_profile_transportationbusiness_registration, null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    company_profile_tradeunion_certificate = models.FileField(upload_to=upload_to_func_company_profile_tradeunion_certificate, null=True, blank=True) # try to use 1:1 rel for upload_to func usage. TODO
    company_profile_introduction = models.CharField(max_length=200, null=True, blank=True)
    company_profile_introduction_video = models.TextField(null=True, blank=True)
    #models.FileField(upload_to="company_introduction_video"+str(upload_to_func_common), null=True, blank=True)
    company_profile_location = models.CharField(max_length=128, null=True, blank=True)
    company_profile_companylocation = models.CharField(max_length=128, null=True, blank=True)
    company_profile_vehiclecount = models.CharField(max_length=8, null=True, blank=True)
    company_code = models.CharField(max_length=12, null=True, blank=True)

    # is_admin = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    # created_on = models.DateTimeField(auto_now_add=True)
    # updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'kingbus_company_profile'
    def __str__(self):
        return str(self.user)

    # objects = UserManager()

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['userid']
    filesavefield = 'companyacc'


# signal/receiver on model creation
def create_profile_model(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created:
        Profile.objects.create(user=instance, nickname=instance.username)

models.signals.post_save.connect(create_profile_model, sender=User,weak=False, dispatch_uid='models.create_profile_model')