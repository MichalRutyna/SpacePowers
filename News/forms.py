import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset
from django.core.validators import MinLengthValidator, MaxLengthValidator

from Nation.models import Nation
from .models import Tag, Post, Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'nation', 'metagame')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-create-comment-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'add_comment/'

        self.fields['nation'].queryset = Nation.objects.filter(owner=user)

        self.helper.add_input(Reset('reset', "Cancel", css_class="btn-outline-danger"))
        self.helper.add_input(Submit('submit', "Comment", css_class='btn-primary'))


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'nation', 'tags')


    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-create-post-form'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        self.fields['nation'].queryset = Nation.objects.filter(owner=user)

        self.helper.add_input(Reset('reset', "Cancel", css_class="btn-outline-danger"))
        self.helper.add_input(Submit('submit', "Post", css_class='btn-primary'))
