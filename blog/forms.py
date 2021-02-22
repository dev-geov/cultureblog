from django.forms import ModelForm, Textarea
from .models import Comment


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['email', 'content']
        widgets = {
            'content': Textarea(attrs={'rows':4, 'cols':15})
        }
