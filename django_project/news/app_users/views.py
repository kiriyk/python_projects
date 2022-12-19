from django.contrib.auth import authenticate, login, logout, models
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView, TemplateView, LogoutView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View, generic

from app_users.forms import AuthForm, RegisterForm, VerifyForm
from app_users.models import Profile


class UserRegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            city = form.cleaned_data.get('city')
            Profile.objects.create(
                user=user,
                city=city,
                phone_number=phone_number,
                is_verified=False
            )
            username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            self.add_user_to_group(user)
            login(request, user)
            return redirect('main-page')
        return render(request, 'users/register.html', {'form': form})

    def add_user_to_group(self, user):
        my_group = models.Group.objects.get(name='Users')
        my_group.user_set.add(user)


class MainPage(TemplateView):
    template_name = 'users/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['views'] = Profile.news_count

        return context


class UsersVerify(PermissionRequiredMixin, TemplateView):
    template_name = 'users/users_verify.html'
    permission_required = 'app_users.change_profile'
    permission_denied_message = 'You have no permission to edit profiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['User'] = Profile.objects.all()
        return context

    def get_success_url(self):
        return reverse('main-page')


class VerifyUpdateView(PermissionRequiredMixin, generic.edit.UpdateView):
    model = Profile
    template_name = 'users/verify_edit.html'
    fields = ['user']
    pk_url_kwarg = 'profile_id'
    permission_required = 'app_users.change_profile'
    permission_denied_message = 'You have no permission to edit profiles'
    success_url = reverse_lazy('users-verify')

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        profile = Profile.objects.get(user=user)
        my_group = models.Group.objects.get(name='Verified users')
        old_group = models.Group.objects.get(name='Users')

        if not profile.is_verified:
            profile.is_verified = True
            profile.save()
            my_group.user_set.add(user)
            old_group.user_set.remove(user)
        else:
            profile.is_verified = False
            profile.save()
            my_group.user_set.remove(user)
            old_group.user_set.add(user)

        return redirect('users-verify')


class NewLogoutView(LogoutView):
    template_name = 'users/logout.html'
    next_page = 'main-page'


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main-page')


class NewLoginView(LoginView):
    template_name = 'users/login.html'
