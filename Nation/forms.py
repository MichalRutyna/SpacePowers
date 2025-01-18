import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Nation


class CreateNationForm(forms.ModelForm):
    name = forms.CharField(
        label="Nation's Name",
        required=True,
        help_text="Other people will see that"
    )
    owner_title = forms.CharField(
        label="How do you want to be titled?",
        required=False,
        help_text="Defaults to glorious leader"
    )
    population = forms.IntegerField(
        label="Initial population",
        required=False,
    )
    PKB = forms.IntegerField(
        label="PKB",
        required=False,
    )

    class Meta:
        model = Nation
        fields = ['name', 'owner_title', 'population', 'PKB']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-nation-creation-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Create nation!'))
