from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *
from web.accounts.form import CreateUserForm


class RegisterView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CreateUserForm
    success_url = reverse_lazy('accounts:login')


# class LoginView(FormView):
#     template_name = 'accounts/login.html'
#     form_class = LoginForm
#     success_url = reverse_lazy('board:list')
#
#     def form_valid(self, form):
#         self.request.session['user'] = form.data.get('email')
#         return super().form_valid(form)
#
#
# def logout(request):
#     if 'user' in request.session:
#         del(request.session['user'])
#     return redirect('accounts:login')
