from django.urls import path
from . import views

urlpatterns = [
    # path('album-detail/<int:pk>', views.AlbumDetailView.as_view(), name='album_detail'),
    # path('album-list/', views.AlbumListView.as_view(), name='album_list'),
    # path('album-list/<int:user_pk>', views.AlbumListView.as_view(), name='album_list_specific'),
    path('create-data-and-caption/', views.DataAndCaptionCreationView.as_view(), name='create_data_and_caption'),
    # path('update-album/<int:pk>', views.AlbumUpdateView.as_view(), name='update_album'),
    # path('delete-album/<int:pk>', views.AlbumDeletionView.as_view(), name='delete_album'),
]