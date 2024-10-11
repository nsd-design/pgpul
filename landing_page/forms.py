from django import forms
from landing_page.models import Post, Temoignage, Partenaire, Comment
from pgpul_admin.forms import TinyMCEWidget


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        content = forms.CharField(widget=TinyMCEWidget(
            attrs={"required": False, "cols": 30, "rows": 20}
        ))

        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Post
        fields = ['title', 'content', 'cover']


class TemoignageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TemoignageForm, self).__init__(*args, **kwargs)

        # Supprimer les labels
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Temoignage
        fields = ['nom', 'avis']


class PartenaireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartenaireForm, self).__init__(*args, **kwargs)

        # Supprimer les labels sur les champs
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Partenaire
        fields = ['denomination', 'logo']


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        # Supprimer les labels sur les champs
        for field_name, field in self.fields.items():
            field.label = ''

    class Meta:
        model = Comment
        fields = ['name', 'content']
