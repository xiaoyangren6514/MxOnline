import re

from django import forms

from operation.models import UserAsk


class UserAskFormOld(forms.Form):
    name = forms.CharField(required=True, min_length=2, max_length=15)
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    course_name = forms.CharField(required=True, min_length=2)


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        PATTREN = r'^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(PATTREN)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号非法', code='mobile_invalid')
