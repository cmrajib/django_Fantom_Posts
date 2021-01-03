from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView

from posts.models import Post
from users.forms import RegisterForm, UserProfileForm
from users.models import UserProfile


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/'

# set this two line in projects settings.py
# LOGOUT_REDIRECT_URL = '/'
# LOGIN_REDIRECT_URL = '/'

class UserLoginView(LoginView):
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    template_name = 'users/login.html'


@method_decorator(login_required(login_url='users/login'),name="dispatch")
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    template_name = 'users/profile-update.html'
    form_class = UserProfileForm


    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save
        return super(UserProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('users:update_profile',kwargs={'slug': self.object.slug})

# A user can not update others profile
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')

        return super(UserProfileUpdateView, self).get(request, *args, **kwargs)



# displaying user profile
@method_decorator(login_required(login_url='users/login'),name="dispatch")
class UserProfileView(ListView):
    template_name = 'users/my-profile.html'
    model = Post
    context_object_name = 'userposts'
    paginate_by = 5


    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['userprofile'] = UserProfile.objects.get(user=self.request.user)
        return context

# Posts, belong to a particular user, can be viewed. Others users post can not be viewed.
    def get_queryset(self):
        return Post.objects.filter(user=self.request.user).order_by('-id')


# To view others posted contents
class UserPostView(ListView):
    template_name = 'users/user-post.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 5

# Querying others post other than current user.
    def get_queryset(self):
        return Post.objects.filter(user=self.kwargs['pk'])