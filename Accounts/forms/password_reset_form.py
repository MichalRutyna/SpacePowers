from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import django.contrib.auth.forms as authforms
import django.forms as forms

class PasswordResetFormCustom(authforms.PasswordResetForm):
    email = forms.EmailField(
        label="Email address:",
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-reset-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Reset password'))

class SetPasswordFormCustom(authforms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-set-new-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Set new password'))