from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from questions.utils import crop_square
from questions.models import Profile, Question, Answer, Tag


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        # Add all the fields you want a user to change
        fields = ('first_name', 'last_name', 'email')


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ('about', 'avatar')

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'png']):  # гифки идут нахер!
                raise ValidationError(_('Please use a JPEG or PNG image.'))

            # validate file size
            if len(avatar) > (1024 * 1024):
                raise ValidationError(_('Avatar file size may not exceed 1M.'))
            avatar.file = crop_square(avatar, sub)

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class NewQuestionForm(forms.ModelForm):
    tags = forms.CharField(required=True, max_length=255)

    class Meta:
        model = Question
        fields = ('title', 'content', 'tags',)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if not tags:
            raise ValidationError(_('You need type at least one tag'))
        elif len(tags.split(',')) > 5:
            raise ValidationError(_('Max 5 tags allowed'))

        return tags


class NewAnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ('content',)
