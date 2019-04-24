from django.contrib.auth.models import User
from django import forms
from .models import Profile


# This form handles users' credentials for the registration process
class UserForm(forms.ModelForm):
    password = forms.CharField()
    password_confirmation = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # Disable Django's default help_text
        for fieldname in ['username', 'password']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:  # For password verification purposes
            raise forms.ValidationError(
                "Password does not match"
            )


# This form handles users' personal information for the registration process
class ProfileForm(forms.ModelForm):
    job_title = forms.CharField(max_length=500, required=True)
    company = forms.CharField(max_length=500, required=True)
    birth_date = forms.DateField(required=True, help_text="Format: DD/MM/YYYY",
                                 widget=forms.DateInput(format='%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',))
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('job_title', 'company', 'birth_date', 'image')

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.job_title = self.cleaned_data['job_title']
        user.company = self.cleaned_data['company']
        user.birth_date = self.cleaned_data['birth_date']
        user.image = self.cleaned_data['image']

        if commit:
            user.save()

        return user


# This form handles updating users' personal information
class EditProfileForm(forms.ModelForm):
    job_title = forms.CharField(max_length=500, required=True)
    company = forms.CharField(max_length=500, required=True)
    birth_date = forms.DateField(required=True, help_text="Format: DD/MM/YYYY",
                                 widget=forms.DateInput(format='%d/%m/%Y'),
                                 input_formats=('%d/%m/%Y',))
    image = forms.ImageField(help_text="Please re-upload your profile picture")

    class Meta:
        model = Profile
        fields = ('job_title', 'company', 'birth_date', 'image')

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        user.job_title = self.cleaned_data['job_title']
        user.company = self.cleaned_data['company']
        user.birth_date = self.cleaned_data['birth_date']
        user.image = self.cleaned_data['image']

        if commit:
            user.save()

        return user


# This form handles users' credentials
class EditCredentialsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
