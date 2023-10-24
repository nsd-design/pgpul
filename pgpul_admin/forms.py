from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms

from utilisateur.models import Utilisateur


class InscriptionForm(forms.ModelForm):
    def __init__(self, *arg, **kwargs):
        super(InscriptionForm, self).__init__(*arg, **kwargs)
        self.helper = FormHelper()
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.helper.layout = Layout(
            Field('password', css_class="form-control", type="password")
        )

        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Utilisateur
        fields = ['first_name', 'last_name', 'email', 'password', 'matricule', 'username']
