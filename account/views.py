from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuth, AccountUpdateform
from blog.models import Post

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_passwoed = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_passwoed)
            login(request, account)
            return redirect('account')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('blog:post_list')


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('blog:post_list')

    if request.POST:
        form = AccountAuth(request.POST)
        if form.is_valid:
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('blog:post_list')
    else:
        form = AccountAuth()
    context['login_form'] = form
    return render(request, 'account/login.html', context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {}
    if request.POST:
        form = AccountUpdateform(request.POST, instance=request.user)
        if form.is_valid:
            form.initial = {
                'email': request.POST['email'],
                'username': request.POST['username'],
            }
            form.save()
            context['succes_message'] = 'Updated'
    else:
        form = AccountUpdateform(
            initial={
                'email': request.user.email,
                'username': request.user.username,
            }
        )
    posts=Post.objects.filter(author=request.user)
    context['account_form'] = form
    context['posts']=posts
    return render(request, 'account/account.html', context)


def must_authenticate_view(request):
    return render(request, 'account/must_authenticate.html', {})
