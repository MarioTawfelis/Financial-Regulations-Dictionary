from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_protect
from accounts.forms import UserForm, ProfileForm, EditProfileForm, EditCredentialsForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile


@csrf_protect
def register(request):
    if request.method == 'POST':  # Check if user is submitting a form
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():  # Perform server-side validation on user inputs
            # Sanitize data by using cleaned_data before storing in database
            # commit=False > do not create the user yet
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data.get('password'))
            user.save()

            user.profile.job_title = profile_form.cleaned_data.get('job_title')
            user.profile.company = profile_form.cleaned_data.get('company')
            user.profile.birth_date = profile_form.cleaned_data.get('birth_date')
            user.profile.image = profile_form.cleaned_data.get('image')
            user.profile.save()

            return redirect(reverse('accounts:view_profile'))
        else:  # If form validation failed, reload form with errors
            print("Form is invalid!")
            content = {'user_form': user_form,
                       'profile_form': profile_form}

    else:  # If it is not a form submission then load form
        user_form = UserForm()
        profile_form = ProfileForm()

        content = {'user_form': user_form,
                   'profile_form': profile_form}

    return render(request, 'accounts/registration_form.html', content)


def login(request):
    if request.method == 'POST':  # This is true if the user has already put in his credentials and clicked Login
        form = LoginForm(request.POST or None)
        # user = authenticate(request, username=username,
        #                     password=password)  # Check if username and password combination are valid
        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
                return redirect('accounts:success')
        else:
            error = True
            return render(request, 'accounts/login', {'form': form})

    elif request.method == 'GET':  # Just load the login form
        return render(request, 'accounts/login')


@login_required
def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk).select_related('profile')  # Find user Profile by user_id
    else:
        user = request.user

    content = {'user': user}
    return render(request, 'accounts/profile.html', content)


@login_required
def edit_profile(request):
    if request.method == 'POST':  # Submit form
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        credentials_form = EditCredentialsForm(request.POST, instance=request.user)

        if profile_form.is_valid() and credentials_form.is_valid():
            profile_form.save()
            credentials_form.save()
            return redirect('accounts:view_profile')
        else:  # If forms are not valid, reload form and show errors
            content = {'profile_form': profile_form,
                       'credentials_form': credentials_form}
            return render(request, 'accounts/edit_profile.html', content)

    else:  # Load form and dynamically initialise form fields using Profile model
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
