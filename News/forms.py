import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset


class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Comment',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-log-in-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'add_comment/'

        self.helper.add_input(Reset('reset', "Cancel", css_class="btn-outline-danger"))
        self.helper.add_input(Submit('submit', "Comment", css_class='btn-primary'))
