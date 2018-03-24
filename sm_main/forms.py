#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from django.core import validators
# from django.core.exceptions import ValidationError
TITLE_CHOICES = (
    ('0', 'classfy'),
    ('1', 'extract'),
    ('2', 'relation'),
)
import json

class MultiField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            raise forms.ValidationError("settings不能为空")
        try:
            value = json.loads(value)
            return value
        except:
            if ',' not in value:
                return value
            else:
                return value.split(',')


class upload_form(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    doc_file = forms.FileField(required=True,error_messages={'required':'请选择要上传的文档'});
    upload_file = forms.FileField(required=True,error_messages={'required':'请选择要上传的样本'});
    name = forms.CharField(required=True,error_messages={'required': 'setting_name不能为空.'})
    settings = MultiField()
    is_single = forms.IntegerField(required=True,error_messages={'required': '请选择是否单选.'})
    setting_type = forms.CharField(
        widget=forms.Select(choices=TITLE_CHOICES)
    )

    def clean_sample_type(self):
        data = self.cleaned_data['setting_type']
        print(data)
        return data


