from django.views.generic import CreateView, UpdateView, DetailView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.db.models import Q
from album.models import Album
from .forms import DataAndCaptionForm
from .models import DataAndCaption
from .mixins import DataAndCaptionUpdateOnlyMixin, OwnerDeleteOnlyMixin
# Create your views here.

user_model = get_user_model()


class DataAndCaptionCreationView(LoginRequiredMixin, CreateView):
    model = DataAndCaption
    form_class = DataAndCaptionForm
    template_name = 'data-and-caption-creation-page.html'
    success_url = reverse_lazy()


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs


    def form_valid(self, form):
        form.instance.owner = self.request.user
        if form.cleaned_data['album'] == None:
            form.instance.album = Album.objects.get_user_uncategorized_data_album()
        return super().form_valid(form)





class AlbumUpdateView(LoginRequiredMixin, DataAndCaptionUpdateOnlyMixin, UpdateView):
    model = DataAndCaption
    form_class = DataAndCaptionForm
    template_name = 'data-and-caption-update-page.html'
    success_url = reverse_lazy()
    pk_url_kwarg = 'pk'


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs


    def form_valid(self, form):
        if form.cleaned_data['album'] == None:
            form.instance.album = Album.objects.get_user_uncategorized_data_album()
        return super().form_valid(form)


# class AlbumListView(LoginRequiredMixin, ListView):
#     model = Album

#     def get_template_names(self):
#         if self.kwargs.get('user_pk') == None:
#             return 'album-list-page.html'
#         else:
#             return 'album-list-specific-page.html'


#     def get_queryset(self):
#         qs = None
#         search_input = self.request.GET.get('search')

#         if self.kwargs.get('user_pk') == None:
#             qs = Album.objects.filter(Q(is_private = False) | Q(owner=self.request.user) & ~Q(name = 'DELETED_DATA_ALBUM'))
#         else:
#             try:
#                 owner = user_model.objects.get(pk=self.kwargs.get('user_pk'))
#                 if owner == self.request.user:
#                     qs = Album.objects.filter(Q(owner=owner))
#                 else:
#                     qs = Album.objects.filter(Q(is_private = False) & Q(owner=owner) & ~Q(name = 'DELETED_DATA_ALBUM'))
#             except user_model.DoesNotExist:
#                 qs = Album.objects.filter(Q(is_private = False) | Q(owner=self.request.user) & ~Q(name = 'DELETED_DATA_ALBUM'))
        
#         if search_input == None:
#             return qs
#         else:
#             qs.filter(Q(name__contains = search_input) | Q(description__contains = search_input))





# class AlbumDetailView(LoginRequiredMixin, OwnerPrivateAccessOrEveryonePublicAccessMixin, DetailView):
#     model = Album
#     template_name = 'album-detail-page.html'

    
#     def get_object(self):
#         qs = Album.objects.filter(Q(pk=self.kwargs.get('pk')) & ~Q(name = 'DELETED_DATA_ALBUM')).select_related('owner')
#         if len(qs) == 0:
#             return None
#         return qs[0]





# class AlbumDeletionView(LoginRequiredMixin, OwnerDeleteOnlyMixin, FormView):
#     model = Album
#     form_class = AlbumDeletionForm
#     template_name = 'album-delete-page.html'
#     success_url = reverse_lazy()


#     def get_object(self):
#         try:
#             return Album.objects.get(Q(pk=self.kwargs.get('pk')) & ~Q(name = 'DELETED_DATA_ALBUM'))
#         except Album.DoesNotExist:
#             raise Http404


#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs.update({'request' : self.request})
#         return kwargs


#     def form_valid(self, form):
#         self.get_object().delete()
#         return super().form_valid(form)