import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from Nation.models import Nation, Army


class NationCreateForm(forms.ModelForm):
    owner_title = forms.CharField(
        label="How do you want to be titled?",
        required=False,
        help_text="Defaults to glorious leader"
    )

    class Meta:
        model = Nation
        fields = ['name', 'owner_title', 'banner', 'flag', 'coat_of_arms', 'population', 'PKB']
        labels = {
            "name": "Nation's Name",
            "population": "Initial population",
        }
        help_texts = {
            "name": "Other people will see that",
            "banner": "Roughly 3:16 ratio, cropped from the middle",
            "flag": "Any ratio should work fine",
            "coat_of_arms": "Any ratio should work fine",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-nation-creation-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Create nation!'))


class NationEditForm(forms.ModelForm):
    class Meta:
        model = Nation
        fields = ['name', 'banner', 'flag', 'coat_of_arms']
        labels = {
            "name": "Nation's name",
        }
        help_texts = {
            "name": "Other people will see that",
            "banner": "Roughly 3:16 ratio, cropped from the middle",
            "flag": "Any ratio should work fine",
            "coat_of_arms": "Any ratio should work fine",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-nation-edit-form'
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'Save edit'))