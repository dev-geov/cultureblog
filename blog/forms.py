from django import forms


class ContactForm(form.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        field = ['title','content','publish']
