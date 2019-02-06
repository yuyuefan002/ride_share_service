# Create your views here.
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
# from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import send_mail

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            send_mail(
                'Account sign up for Batmobile',
                'Congratulation! You have successfully signed up for BatMobile.\n Your username is: ' + new_user.username + ' Your password is: ' + form.cleaned_data['password1'] + '.\n',
                'BatMobile',
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return redirect('home:loginHome')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

