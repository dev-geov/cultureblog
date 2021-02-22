from django import forms
from blog.models import Post
from .email import Email


class ContactForm(forms.Form):
    subject = forms.CharField(label="Assunto")
    email = forms.CharField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Mensagem")

    mail = Email(
        subject=subject,
        message=message,
        receiver=email,
    )

    def send_email(self):
        if self.mail:
            return True
        
        return False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','publish', 'category']