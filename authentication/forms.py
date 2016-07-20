"""from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm
from django.contrib.auth import get_user_model

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label = 'Подтверждение',
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError('Пароль и подтверждение не совпадают')
        return password2

    def save(self, commit=True):
        account = super(UserCreationForm, self).save(commit=False)
        account.set_password(self.cleaned_data['password1'])
        if commit:
            account.save()
            return account

        class Meta:
            model = get_user_model()
            fields = ('email')

    class UserChangeForm(forms.ModelForm):

        password = ReadOnlyPasswordHashField(
            widget = forms.PasswordInput,
            required=False
        )

        def save(self, commit=True):
            account = super(UserChangeForm, self).save(commit=False)
            password = self.cleaned_data["password"]
            if password:
                account.set_password(password)
            if commit:
                account.save()
            return account
        class Meta:
            model = get_user_model()
            fields = ['email',]

    class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField()
        """
from django import forms
from django.contrib.auth.models import User


class NewUserForm(forms.Form):
    username = forms.CharField(required=True, min_length=5, max_length=20, strip=True)
    password = forms.CharField(required=True, min_length=1, max_length=20, widget=forms.PasswordInput)

    def is_valid(self):
        result = forms.Form.is_valid(self)
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)
        except BaseException:
            user = None
        if user is not None:
            result = False
            self.add_error('username', 'Такой пользователь уже существует')
        return result

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        #for field in self.fields:
           # self.fields[field].widget.attrs['class'] = 'form-control'
            # class PostIngredient(models.Model):
            # post = models.ForeighKey(Post)
            # ingredient = models.ForeignKey(Ingredient)
