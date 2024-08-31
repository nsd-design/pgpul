from django import forms
from landing_page.models import Post
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