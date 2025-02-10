from django import forms
from .models import utilisateur,mess
from django.contrib.auth.models import User
class UtilForm2(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","last_name","first_name","email","password"]
    def __init__(self, *args, **kwargs):
        super(UtilForm2, self).__init__(*args, **kwargs)
        # then do extra stuff:
        self.fields['username'].help_text = ''
        self.fields['last_name'].help_text = ''
        self.fields['first_name'].help_text = ''
        self.fields['email'].help_email = ''
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': ''})
        self.fields['password'].widget.attrs['class'] = 'form-control'

class MessagesForm(forms.ModelForm):
    class Meta:
        model=mess
        fields='__all__'
    #def __init__(self, *args, **kwargs):
    #    super(MessagesForm, self).__init__(*args, **kwargs)
     #   # then do extra stuff:
      #  self.fields['sender'].help_text = ''
       # self.fields['emails'].help_email = ''
        #self.fields['msg'].help_text = ''
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')

class UtilForm(forms.ModelForm):
    class Meta:
        model=utilisateur
        fields=["nom","prenom","email","pw"]
    def __init__(self, *args, **kwargs):
        super(UtilForm, self).__init__(*args, **kwargs)
        # then do extra stuff:
        self.fields['nom'].help_text = ''
        self.fields['prenom'].help_text = ''
        self.fields['email'].help_email = ''
        self.fields['pw'].widget = forms.PasswordInput(attrs={'placeholder': ''})
        self.fields['pw'].widget.attrs['class'] = 'form-control'

# authentication/forms.py
from django import forms