from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms

from pgpul_admin.models import *
from utilisateur.models import Utilisateur


# class InscriptionForm(forms.ModelForm):
#     def __init__(self, *arg, **kwargs):
#         super(InscriptionForm, self).__init__(*arg, **kwargs)
#         self.helper = FormHelper()
#         self.fields['first_name'].required = True
#         self.fields['last_name'].required = True
#         self.fields['email'].required = True
#
#         self.helper.layout = Layout(
#             Field('password', css_class="form-control", type="password")
#         )
#
#         # Supprimer les labels
#         for field_name, field in self.fields.items():
#             field.label = ''

    # class Meta:
    #     model = Utilisateur
    #     fields = ['first_name', 'last_name', 'email', 'password', 'matricule', 'username']


class FaculteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FaculteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        # Definir les placeholders
        self.fields['nom_fac'].widget.attrs['placeholder'] = 'entrez le nom de la faculté'
        self.fields['code_fac'].widget.attrs['placeholder'] = 'entrez le code de la faculté'

        self.fields['code_fac'].widget.attrs['min'] = 1
        self.fields['code_fac'].widget.attrs['max'] = 99

        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''
    class Meta:
        model = Faculte
        fields = ['nom_fac', 'code_fac']


class DepartementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DepartementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

         # Definir les placeholders
        self.fields['nom_dept'].widget.attrs['placeholder'] = "entrez le nom du département"
        self.fields['code_dept'].widget.attrs['placeholder'] = "entrez le code du département"

        self.fields['code_dept'].widget.attrs['min'] = 1
        self.fields['code_dept'].widget.attrs['max'] = 99
        
        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Departement
        fields = ['nom_dept', 'code_dept', 'dept_fac']


class ClassForm(forms.ModelForm):
    def __init__(self, *args, **kwarg):
        super(ClassForm, self).__init__(*args, **kwarg)
        self.helper = FormHelper()

        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Classe
        fields = ['designation']


class MatiereForm(forms.ModelForm):
    def __init__(self, *args, **kwarg):
        super(MatiereForm, self).__init__(*args, **kwarg)
        self.helper = FormHelper()
        self.fields['nom_mat'].widget.attrs['placeholder'] = 'entrez le nom de la matière'

        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Matiere
        fields = ['nom_mat', 'classe_mat', 'dept_mat']


class EnseignantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EnseignantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Enseignant
        fields = ["genre_ens", "tel_ens", "specialite_ens",
                  "departement_principal", "adresse_en",
                  "first_name", "last_name", "email"
                  ]
