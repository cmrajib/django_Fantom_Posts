from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import UserProfile


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# This is for updating user profile. single-input class is applied to the HTML
# input field when creating birth_day, bio and image fields for updating profile.
class UserProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.field_class = 'mt-10'
        self.helper.layout = Layout(
            Field("birth_day",css_class="single-input"),
            Field("bio",css_class="single-input"),
            Field("image",css_class="single-input"),

        )


# CSS class "genric-btn success-border medium" is applied to the submit button
        self.helper.add_input(Submit('submit','Update',css_class="genric-btn success-border medium"))


# widgets is for date picker. User can select a date from calendar.
    class Meta:
        model = UserProfile
        fields = ('birth_day','bio','image')
        widgets = {
            'birth_day':forms.DateInput(attrs={'type':'date'})
        }