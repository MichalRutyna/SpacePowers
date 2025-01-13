from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import django.forms as forms

class ExampleForm(forms.Form):
    mail = forms.EmailField(
        label="Email address",
        required=True,
        initial="foo@bar.com",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-password-reset-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.add_input(Submit('submit', 'Reset password'))