from django.urls import path
from . import views

urlpatterns = [
    path('account-profile/<int:pk>', views.UserAccountProfileView.as_view(), name='user_profile'),
    path('account-list/', views.UserAccountListView.as_view(), name='user_list'),
    path('create-account/', views.UserAccountCreationView.as_view(), name='create_account'),
    path('update-account/', views.UserAccountUpdateView.as_view(), name='update_account'),
    path('delete-account/', views.UserAccountDeletionView.as_view(), name='delete_account'),
    path('change-password/', views.UserAccountChangePasswordView.as_view(), name='change_password'),
    path('log-in/', views.LoginView.as_view(), name='log_in'),
    path('log-out/', views.LogoutView.as_view(), name='log_out'),
]