from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):

    user = request.user
    if user.is_authenticated():
        return render(request, 'index.html')

    return redirect('/login/')


@login_required
def logout_user(request):
    logout(request)
    return redirect('/')