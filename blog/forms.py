from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import Comment


class PostForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '400px'}}))


class CommentForm(forms.Form):
    commentary_text = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows': 4}))