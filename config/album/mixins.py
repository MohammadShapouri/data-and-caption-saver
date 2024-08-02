from django.http import HttpResponse
from django.db.models import Q
from .models import Album


class OwnerUpdateOnlyMixin:
    def get_album(self, pk):
        try:
            return Album.objects.get(Q(pk = pk) & ~Q(name = 'DELETED_DATA_ALBUM'))
        except Album.DoesNotExist:
            return None


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400, content="You are not logged in.")
        else:
            album = self.get_album(kwargs.get('pk'))
            if album != None and int(request.user.pk) != int(album.owner.pk):
                return HttpResponse(status=400, content="You can't update this album.")
            else:
                return super().dispatch(request, *args, **kwargs)





class OwnerPrivateAccessOrEveryonePublicAccessMixin:
    def get_album(self, pk):
        try:
            return Album.objects.get(Q(pk=pk) & ~Q(name = 'DELETED_DATA_ALBUM'))
        except Album.DoesNotExist:
            return None


    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=400, content="You are not logged in.")
        else:
            album = self.get_album(kwargs.get('pk'))
            if album != None and int(request.user.pk) != int(album.owner.pk) and album.is_private:
                return HttpResponse(status=400, content="You can't access this album.")
            else:
                return super().dispatch(request, *args, **kwargs)





class OwnerDeleteOnlyMixin(OwnerUpdateOnlyMixin):
    pass