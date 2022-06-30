from django.shortcuts import redirect, render

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from api.models import GroupMember

# Create your views here.
class CustomLoginView(LoginView):
    template_name='login/login.html'
    fields='__all__'
    redirect_authenticated_user= True

    def get_success_url(self):
        return reverse_lazy('group-list')

class RegisterPage(FormView):
    template_name='login/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user=True
    success_url= reverse_lazy('group-list')

    def form_valid(self,form):
        user=form.save()
        GroupMember.objects.create(user=user)
        if user is not None:
            login(self.request, user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('group-list')
        return super(RegisterPage,self).get(*args,**kwargs)


