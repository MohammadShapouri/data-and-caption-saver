from django.views.generic import CreateView, UpdateView, FormView, DetailView, ListView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .forms import (
                    UserAccountCreationForm,
                    UserAccountUpdateForm,
                    UserAccountDeletionForm,
                    LoginForm,
                    PasswordChangeForm,
                    PasswordResetForm
                    )

# Create your views here.

user_model = get_user_model()

class UserAccountProfileView(LoginRequiredMixin, DetailView):
    model = user_model
    template_name = 'user-profile-page.html'
    pk_url_kwarg = 'pk'

    def get_object(self):
        try:
            return user_model.objects.get(Q(pk=self.kwargs.get(self.pk_url_kwarg)) & Q(is_discoverable=True)) 
        except user_model.DoesNotExist:
            return None





class UserAccountListView(LoginRequiredMixin, ListView):
    model = user_model
    template_name = 'user-list-page.html'

    def get_queryset(self):
        search_input = self.request.GET.get('search')
        if search_input == None:
            qs = user_model.objects.filter(Q(is_discoverable=True))
        else:
            qs = user_model.objects.filter(Q(is_discoverable=True) & Q(username__contains=search_input) | Q(first_name__contains=search_input) | Q(last_name__contains=search_input))
            print(qs)
        if len(qs) > 0:
            return qs
        else:
            return None





class UserAccountCreationView(CreateView):
    model = user_model
    template_name = 'user-registeration-page.html'
    form_class = UserAccountCreationForm
    success_url = reverse_lazy('log_in')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs





class UserAccountUpdateView(LoginRequiredMixin, UpdateView):
    model = user_model
    template_name = 'user-update-page.html'
    form_class = UserAccountUpdateForm
    success_url = reverse_lazy('log_in')

    def get_object(self):
        return self.request.user


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs


    # def get(self, request, *args, **kwargs):
    #     data = {
    #         "form": UserAccountUpdateForm(request.user)
    #     }
    #     return render(request, 'user-update-page.html', data)


    # def post(self, request, *args, **kwargs):
    #     form = UserAccountUpdateForm(request.POST, request.user, request=self.request)
    #     if form.is_valid():
    #         form.save()
    #         return reverse_lazy('log_in')
    #     data = {
    #         "form": form
    #     }
    #     return render(request, 'user-update-page.html', data)





class UserAccountChangePasswordView(LoginRequiredMixin, FormView):
    model = user_model
    template_name = 'user-change-password-page.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy()


    def get_object(self):
        return self.request.user


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request' : self.request})
        return kwargs


    def form_valid(self, form):
        new_password = form.cleaned_data['new_password1']
        self.request.user.password = make_password(password=new_password)
        self.request.user.save()
        return super().form_valid(form)





class UserAccountDeletionView(LoginRequiredMixin, FormView):
    template_name = 'user-deletion-page.html'
    form_class = UserAccountDeletionForm
    success_url = reverse_lazy('log_in')


    def get_object(self, queryset):
        return self.request.user


    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        username = self.request.user.username

        user = authenticate(self.request, username=username, password=password)
        if user is None:
            form.add_error('password', "The given information is not correct.")
            return super().form_invalid(form)
        else:
            user.delete()
        return super().form_valid(form)





class LoginView(FormView):
    form_class = LoginForm
    template_name = 'user-login-page.html'
    success_url = reverse_lazy('log_in')


    def form_valid(self, form):
        username_email = form.cleaned_data.get('username_email')
        password = form.cleaned_data.get('password')

        if str(username_email).__contains__('@'):
            email = username_email
            try:
                requested_user = user_model.objects.get(email__iexact = email)
            except user_model.DoesNotExist:
                form.add_error('detail', "The given information is not correct.")
                return super().form_invalid(form)
            user = authenticate(self.request, username=requested_user.username, password=password)
            if user is None:
                form.add_error('detail', "The given information is not correct.")
                return super().form_invalid(form)
            else:
                login(self.request, user)
        else:
            username = username_email
            try:
                requested_user = user_model.objects.get(username__iexact = username)
            except user_model.DoesNotExist:
                form.add_error('username_email', "The given information is not correct.")
                return super().form_invalid(form)

            user = authenticate(self.request, username=requested_user.username, password=password)
            if user is None:
                form.add_error('password', "The given information is not correct.")
                return super().form_invalid(form)
        return super().form_valid(form)





class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('log_in')
