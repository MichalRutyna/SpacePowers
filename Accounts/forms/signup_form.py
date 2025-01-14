from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import django.contrib.auth.forms as authforms
import django.forms as forms
from django.contrib.auth.models import User


class CreateUserForm(authforms.UserCreationForm):
    username = forms.CharField(
        label="Username",
        required=True,
        help_text="Login for the account"
    )

    email = forms.EmailField(
        label="Email",
        required=False,
        help_text="Used only for password recovery"
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-user-creation-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Create account'))
