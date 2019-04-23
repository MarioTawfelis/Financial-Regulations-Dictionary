from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_protect
from accounts.forms import UserForm, ProfileForm, EditProfileForm, EditCredentialsForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile


@csrf_protect
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data.get('password'))
            user.save()

            user.profile.job_title = profile_form.cleaned_data.get('job_title')
            user.profile.company = profile_form.cleaned_data.get('company')
            user.profile.birth_date = profile_form.cleaned_data.get('birth_date')
            user.profile.image = profile_form.cleaned_data.get('image')
            user.profile.save()

            return redirect(reverse('accounts:view_profile'))
        else:
            print("Form is invalid!")
            content = {'user_form': user_form,
                       'profile_form': profile_form}

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
        profile = Profile.objects.get(user=request.user)
        profile_data = {'profile': profile}
        profile_form = EditProfileForm(initial=profile_data)
        credentials_form = EditCredentialsForm(instance=user)
        content = {'profile_form': profile_form,
                   'credentials_form': credentials_form}
        return render(request, 'accounts/edit_profile.html', content)


@login_required
def logout(request):
    logout(request)
