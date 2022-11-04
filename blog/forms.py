from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('html_content',)
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 450px; align: center;",
                    "placeholder": "Title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 900px;",
                    "placeholder": "Content",
                }
            ),
        }

class CustomFeedsForm(forms.Form):
    name = forms.CharField(max_length=64)
    filter = forms.CharField(max_length=256)
    class Meta:
        widgets = {
            "name": forms.TextInput(),
            "filters": forms.TextInput(),
        }

class ArticleMarkdownForm(forms.Form):
    markdown_content = forms.CharField(widget=forms.Textarea)
    class Meta:
        widgets = {
            "markdown_content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 900px;",
                    "placeholder": "Content",
                }
            ),
        }
