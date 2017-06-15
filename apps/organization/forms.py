from django import forms

from operation.models import UserAsk


class UserAskForm(forms.Form):
    name = forms.CharField(required=True, min_length=2, max_length=15)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    course_name = forms.CharField(required=True, min_length=2)


class UserAskFormNew(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']
