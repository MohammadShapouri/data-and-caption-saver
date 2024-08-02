from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils.validators.username_validator import custom_ASCII_username_validator
# Create your models here.


def define_account_photos_directory(instance, filename):
    file_date_time = timezone.now().strftime('%Y%m%d%h%m%s')
    return "photos/account_photos/{0}/{1}_{2}".format(instance.username, file_date_time, filename)

class UserAccount(AbstractUser):
    first_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="First Name")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Last Name")
    username = models.CharField(max_length=100, unique=True, blank=False, null=False, validators=[custom_ASCII_username_validator], verbose_name="Username")
    email = models.EmailField(max_length=200, unique=True, blank=False, null=False, verbose_name="Email")
    profile_picture = models.ImageField(default='photos/account_photos/default/default_profile_pic.png', upload_to=define_account_photos_directory, verbose_name="Profile Picture")
    is_private = models.BooleanField(default=False, blank=False, null=False, verbose_name="Is Account Private?")
    is_discoverable = models.BooleanField(default=True, blank=False, null=False, verbose_name="Is Account Discoverable?")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    class Meta:
        verbose_name = "User Account"
        verbose_name_plural = "User Accounts"

    def __str__(self):
        return self.username

    def is_there_any_new_email(self):
        return self.new_email != None # Means there is a new email.

    def is_new_email_validated(self):
        return self.new_email == None # Means it's validated.