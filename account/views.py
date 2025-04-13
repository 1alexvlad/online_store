from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


from orders.models import Order

from .forms import LoginForm, UserCreateForm

User = get_user_model()


class RegistrationView(CreateView):
    template_name = 'account/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('product:index')

    def form_valid(self, form):
        user = form.save()
        user.save()
        
        auth.login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')

        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context  
    


class UserLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('product:index')
    
    def form_valid(self, form):

        user = form.get_user()

        if user:
            auth.login(self.request, user)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context   
    
    
@login_required
def logout_user(request):
    auth.logout(request)
    return redirect('product:index')


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'account/profile.html'
    context_object_name = 'orders'
    login_url = 'account:login'
    
    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        ).prefetch_related('order_items').order_by('-created_timestamp')



class UsersCart(TemplateView):
    template_name = 'account/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context