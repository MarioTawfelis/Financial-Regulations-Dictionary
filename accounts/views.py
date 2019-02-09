from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_protect

from accounts.forms import UserForm, ProfileForm, EditProfileForm, EditCredentialsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@csrf_protect
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() or profile_form.is_valid():
            user = user_form.save(commit=False)
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            email = user_form.cleaned_data['email']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return redirect(reverse('accounts:view_profile'))

        content = {'user_form': user_form,
                   'profile_form': profile_form}

        return render('accounts/registration_form.html', content)

    else:
        user_form = UserForm()
        profile_form = ProfileForm()

        content = {'user_form': user_form,
                   'profile_form': profile_form}
        return render(request, 'accounts/registration_form.html', content)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accounts:success')
        else:
            return redirect('accounts:login')

    elif request.method == 'GET':
        return render(request, 'accounts/login')


@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk).select_related('profile')
    else:
        user = request.user

    content = {'user': user}
    return render(request, 'accounts/profile.html', content)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        credentials_form = EditCredentialsForm(request.POST, instance=request.user)

        if profile_form.is_valid() and credentials_form.is_valid():
            profile_form.save()
            credentials_form.save()
            return redirect('accounts:view_profile')
        else:
            return redirect('accounts:edit_profile')

    else:
        user = request.user
        profile_form = EditProfileForm(instance=user.profile)
        credentials_form = EditCredentialsForm(instance=user)
        content = {'profile_form': profile_form,
                   'credentials_form': credentials_form}
        return render(request, 'accounts/edit_profile.html', content)


@login_required
def logout(request):
    logout(request)
