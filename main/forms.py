from django import forms
from .models import *
import re
from django.contrib.auth.hashers import check_password

# создадим откомпилированный шаблон регулярного выражения
# \w - соответствует любой букве, цифре или символу нижнего подчеркивания
t_englishWord = re.compile(r"^[a-zA-Z][a-zA-Z\d_]+$", re.U)
t_name = re.compile(r"^[A-Z][a-z]+$", re.U)


def isEnglishWord(word):
    return t_englishWord.search(word)


def isName(name):
    return t_name.search(name)


class AddRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, strip=True, label="Username",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Your username",
                                                             "type": "text"}))

    email = forms.EmailField(max_length=50, required=True, label="Email",
                             widget=forms.TextInput(attrs={"class": "form-control",
                                                           "placeholder": "Email",
                                                           "type": "email"}))

    first_name = forms.CharField(max_length=150, required=True, strip=True, label="First name",
                                 widget=forms.TextInput(attrs={"class": "form-control",
                                                               "placeholder": "Your name",
                                                               "type": "text"}))

    last_name = forms.CharField(max_length=150, required=True, strip=True, label="Second name",
                                widget=forms.TextInput(attrs={"class": "form-control",
                                                              "placeholder": "Your last name",
                                                              "type": "text"}))

    password = forms.CharField(max_length=128, required=True, strip=True, label="Password",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "type": "password"}))

    repeat_password = forms.CharField(max_length=128, required=True, strip=True, label="Repeat password",
                                      widget=forms.TextInput(attrs={"class": "form-control",
                                                                    "type": "password"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        has_normal_size = 8 <= len(username) <= 150
        if not isEnglishWord(username) or not has_normal_size:
            self.cleaned_data['password'] = ""
            self.cleaned_data['repeat_password'] = ""
            raise forms.ValidationError(
                "Username must contain 8 or more characters: a-z/(A-Z), 0-9, _ and begin with a letter", code=1
            )
        if User.objects.filter(username=username).count() > 1:
            raise forms.ValidationError(
                "This username already in use. Please write another", code=1
            )
        return username

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not isName(last_name):
            self.cleaned_data['password'] = ""
            self.cleaned_data['repeat_password'] = ""
            raise forms.ValidationError(
                "Last name must begin with a capital letter and contain characters: a-z", code=3
            )
        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not isName(first_name):
            self.cleaned_data['password'] = ""
            self.cleaned_data['repeat_password'] = ""
            raise forms.ValidationError(
                "First name must begin with a capital letter and contain characters: a-z", code=3
            )
        return first_name

    def clean(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        if password != repeat_password:
            self.cleaned_data['password'] = ""
            self.cleaned_data['repeat_password'] = ""
            raise forms.ValidationError(
                "Passwords mismatch", code=2
            )

    def save(self):
        # данные с формы
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        # создадим и сохраним в бд юзера
        user = User.objects.create_user(username=username, email=email, password=password)

        # данные не с формы
        last_login = datetime.now()
        user.first_name = first_name
        user.last_name = last_name
        user.last_login = last_login
        user.date_joined = last_login
        user.save()
        Profile.objects.create(user=user, avatar='users/default.jpg')
        return User


class AddAuthorizationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, strip=True, label="Username",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Your username",
                                                             "type": "text"}))

    password = forms.CharField(max_length=128, required=True, strip=True, label="Password",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "type": "password"}))

    def clean_username(self):
        username = self.cleaned_data['username']
        has_normal_size = 8 <= len(username) <= 150
        if not isEnglishWord(username) or not has_normal_size:
            self.cleaned_data['password'] = ""
            raise forms.ValidationError(
                "Username must contain 8 or more characters: a-z/(A-Z), 0-9, _ and begin with a letter", code=1
            )
        if User.objects.filter(username=username).count() > 1:
            raise forms.ValidationError(
                "This username already in use. Please write another", code=1
            )
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        has_normal_size = len(password) >= 8
        if not has_normal_size:
            self.cleaned_data['password'] = ""
            raise forms.ValidationError(
                "Password must contain 8 or more characters", code=4
            )
        return password

    def clean(self):
        # если мы словили exceptions в clean_xxx, этих полей не будет в cleaned_data --> надо обработать
        try:
            username = self.cleaned_data['username']
        except KeyError:
            return

        try:
            password = self.cleaned_data['password']
        except KeyError:
            return

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.add_error(None, forms.ValidationError("User and password are wrong", code=5))
            return

        if not check_password(password, user.password):
            self.add_error(None, forms.ValidationError("User and password are wrong", code=5))
            return


class ChangeProfile(forms.Form):
    username = forms.CharField(max_length=150, required=True, strip=True, label="Username",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "placeholder": "Your username",
                                                             "type": "text"}))

    email = forms.EmailField(max_length=50, required=True, label="Email",
                             widget=forms.TextInput(attrs={"class": "form-control",
                                                           "placeholder": "Email",
                                                           "type": "email"}))

    password = forms.CharField(max_length=128, required=False, strip=True, label="Change password",
                               widget=forms.TextInput(attrs={"class": "form-control",
                                                             "type": "password"}))

    repeat_password = forms.CharField(max_length=128, required=False, strip=True, label="Repeat password",
                                      widget=forms.TextInput(attrs={"class": "form-control",
                                                                    "type": "password"}))

    avatar = forms.ImageField(required=False, label="Upload avatar",
                              widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        has_normal_size = 8 <= len(username) <= 150
        if not isEnglishWord(username) or not has_normal_size:
            self.cleaned_data['password'] = ""
            raise forms.ValidationError(
                "Username must contain 8 or more characters: a-z/(A-Z), 0-9, _ and begin with a letter", code=1
            )
        if User.objects.filter(username=username).count() > 1:
            raise forms.ValidationError(
                "This username already in use. Please write another", code=1
            )
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if password == "":
            return password
        has_normal_size = len(password) >= 8
        if not has_normal_size:
            self.cleaned_data['password'] = ""
            raise forms.ValidationError(
                "Password must contain 8 or more characters", code=4
            )
        return password

    def clean(self):
        try:
            password = self.cleaned_data['password']
            repeat_password = self.cleaned_data['repeat_password']
        except KeyError:
            return

        if password == repeat_password and password == "":
            return
        if password != repeat_password:
            self.cleaned_data['password'] = ""
            self.cleaned_data['repeat_password'] = ""
            raise forms.ValidationError(
                "Passwords mismatch", code=2
            )

    def save(self, user_id):
        user = User.objects.get(id=user_id)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if self.cleaned_data['password'] != "":
            user.set_password(self.cleaned_data['password'])

        profile = Profile.objects.get(user=user_id)
        if self.cleaned_data['avatar']:
            profile.avatar = self.cleaned_data['avatar']
        user.save()
        profile.save()
