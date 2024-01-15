from django import forms
from .models import *
import re
from django.contrib.auth.hashers import check_password

# создадим откомпилированный шаблон регулярного выражения
# \w - соответствует любой букве, цифре или символу нижнего подчеркивания
t_englishWord = re.compile(r"^[a-zA-Z][a-zA-Z\d_]+$", re.U)
t_name = re.compile(r"^[A-Z][a-z]+$", re.U)
t_tags = re.compile(r'^([A-Za-z]+\s*,\s*){0,2}([A-Za-z]+\s*)?$', re.U)


def isEnglishWord(word):
    return t_englishWord.search(word)


def isName(name):
    return t_name.search(name)


def isCorrectTags(tags):
    return t_tags.search(tags)


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
        return user


class AddQuestionForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=150, required=True, strip=True, label="Title",
                            widget=forms.TextInput(attrs={"class": "col-12 py-1 form-control",
                                                          "placeholder": "e.g. Is there an R function for finding "
                                                                         "the index of an element in a vector?"}),
                            help_text="Be specific and imagine you’re asking a question to another person.")

    text = forms.CharField(min_length=20, required=True, strip=True, label="Body",
                           widget=forms.Textarea(attrs={"class": "col-12 py-1 form-control", "rows": 6,
                                                        "placeholder": "Minimum 20 characters. Good luck!"}),
                           help_text="Introduce the problem and expand on what you put in the title. "
                                     "Minimum 20 characters.")

    tags = forms.CharField(required=False, strip=True, label="Tags",
                           widget=forms.TextInput(attrs={"class": "col-12 py-1 form-control", "rows": 6,
                                                         "placeholder": " e.g. (windows, database, vga)"}),
                           help_text="Add up to 3 tags to describe what your question is about. Start typing to see suggestions.")

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3 or len(title) > 150:
            raise forms.ValidationError(
                "Title must contain minimum 3 and maximum 150 characters"
            )
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 20:
            raise forms.ValidationError(
                "Text must contain minimum 20 characters"
            )
        return text

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not isCorrectTags(tags):
            raise forms.ValidationError(
                "Maximum 3 tags and they must be separated with comma"
            )
        return tags

    def save(self, user):
        try:
            title = self.cleaned_data['title']
            text = self.cleaned_data['text']
            tags = self.cleaned_data['tags']
        except KeyError:
            return None

        # разобьем строку tags на массив тегов и добавим каждый тег к вопросу и в таблицу, если он раннее не существовал
        tags_list = tags.split(', ')
        question = Question.objects.create(user=user, title=title, text=text)
        for t in tags_list:
            tag, created = Tag.objects.get_or_create(name=t)
            question.tags.add(tag)

        return question


class AddAnswerForm(forms.Form):
    text = forms.CharField(min_length=3, required=True, strip=True, label="Your answer",
                           widget=forms.Textarea(attrs={"class": "col-12 py-1 form-control", "rows": 6}),
                           help_text="Introduce the problem and expand on what you put in the title. "
                                     "Minimum 20 characters.")

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 3:
            raise forms.ValidationError(
                "text must contain minimum 3 characters"
            )
        return text

    def save(self, question_id, user):
        text = self.cleaned_data['text']
        q = Question.objects.get(id=question_id)
        return Answer.objects.create(text=text, question=q, user=user)
