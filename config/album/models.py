from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model
# Create your models here.

user_model = get_user_model()


class AlbumManager(models.Manager):
    def get_user_uncategorized_data_album(self, user):
        try:
            return Album.objects.get(Q(owner = user) & Q(name = 'UNCATEGORIZED_DATA_ALBUM'))
        except Album.DoesNotExist:
            return Album.objects.create(Q(owner = user) & Q(name = 'UNCATEGORIZED_DATA_ALBUM'))



def define_album_photos_directory(instance, filename):
    file_date_time = timezone.now().strftime('%Y%m%d%h%m%s')
    return "photos/album_photos/{0}/{1}/{2}_{3}".format(instance.owner.username, instance.pk, file_date_time, filename)

class Album(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Album Name")
    owner = models.ForeignKey(user_model, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Owner")
    description = models.TextField(max_length=200, blank=True, null=True, verbose_name="Album Description")
    album_picture = models.ImageField(default='photos/album_photos/default/default_album_pic.png', upload_to=define_album_photos_directory, verbose_name="Profile Picture")
    is_private = models.BooleanField(default=False, blank=False, null=False, verbose_name="Is Album Private?")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    objects = AlbumManager()

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albums"

    def __str__(self):
        return self.name
