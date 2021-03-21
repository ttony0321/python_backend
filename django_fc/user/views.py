from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import  make_password
from .models import User
# Create your views here.


def index(request):
    return render(request, 'index.html', {'email': request.session.get('user')})#세션 안의 유저를 가져옴


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
            level='user'
            )
        user.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        self.request.session['user'] = form.data.get('email')#로그인한 이메일을 session 에 저장

        return super().form_valid(form)#기존의 form_valid함수 호출

def logout(request):
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')