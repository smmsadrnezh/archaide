from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(label=_('Password'), widget=forms.PasswordInput, required=True)
#     password2 = forms.CharField(label=_('Repeat Password'), widget=forms.PasswordInput, required=True)
#
#     class Meta:
#         model = User
#         fields = ('email', 'username')
#
#     def clean_password2(self):
#         if self.cleaned_data['password'] != self.cleaned_data['password2']:
#             raise forms.ValidationError(_('Passwords do\'nt match'))
#         return self.cleaned_data['password2']
