from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from album.models import Album
# Create your models here.

user_model = get_user_model()

def define_files_directory(instance, filename):
    file_date_time = timezone.now().strftime('%Y%m%d%h%m%s')
    return "files/{0}/{1}_{2}".format(instance.owner.username, file_date_time, filename)

class DataAndCaption(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name="Title")
    file = models.FileField(upload_to=define_files_directory, blank=True, null=True, verbose_name="File")
    url = models.CharField(max_length=250, blank=True, null=True, verbose_name="URL")
    owner_description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Owner's Description")
    ai_based_description = models.TextField(max_length=500, blank=True, null=True, verbose_name="AI-based Description")
    owner = models.ForeignKey(user_model, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Owner")
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Album")
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Update Date")

    class Meta:
        verbose_name = "File and Caption"
        verbose_name_plural = "Files and Captions"

    def __str__(self):
        return str(self.owner) + ' - ' + str(self.title)
