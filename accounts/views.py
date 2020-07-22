from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render


def sign_in(request):
    if request.method == "POST":
        # TODO : correct this code
        user = authenticate(username=User.objects.get(email=request.POST.get('email', '')).username,
                            password=request.POST.get('password', ''))
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'sign_in.html', {'success': False})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'sign_in.html', {'success': True})


def sign_out(request):
    logout(request)
    return redirect(sign_in)


def register(request):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password2 != password:
            return render(request, 'register.html', {'not_match_password': True})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'duplicate_user': True})

        User.objects.create_user(username=email, email=email, password=password)
        return render(request, 'sign_in.html', {'success': True, 'register_success': True})
    else:
        return render(request, 'register.html', {'success': True})
