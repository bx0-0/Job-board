from django import forms
from .models import Apply, Job
from django.db import transaction


@transaction.atomic
class ApplyForm(forms.ModelForm):
    cv = forms.FileField(disabled=True, label='Please note that cv will  automatically be uploaded ',required=False)

    class Meta:
        model = Apply
        fields = ["name", "mail", "url", "info_for_applier"]


class AddNewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        exclude = [
            "slug",
            "CreateBy",
        ]
