import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render


def sign_in(request):
    context = {}
    if request.method == "POST":
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        ''' End reCAPTCHA validation '''
        if result['success']:
            context['true_captcha'] = True
            try:
                user = authenticate(username=User.objects.get(email=request.POST.get('email', '')).username,
                                    password=request.POST.get('password', ''))
            except ObjectDoesNotExist:
                context['success'] = False
                return render(request, 'sign_in.html', context)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                context['success'] = False
                return render(request, 'sign_in.html', context)
        else:
            context['true_captcha'] = False
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            context['success'] = True
            return render(request, 'sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('accounts:sign_in')


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
