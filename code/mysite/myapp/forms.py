from django import forms
from . import models

class IssueForm(forms.Form):
    title = forms.CharField(
        label='title',
        required=True,
        max_length=100
    )

    description = forms.CharField(
        label='description',
        widget=forms.Textarea,
        required=False,
        max_length=240
    )

    issue_type = forms.IntegerField(
        label='issue_type',
        required=True
    )

    date_created = forms.CharField(
        label='date_created',
        required=True,
    )

    assigned_user = forms.CharField(
        label='assigned_user',
        required=False,
        max_length=50
    )

    affected_user = forms.CharField(
        label='affected_user',
        required=True,
        max_length=50,
    )

    is_solved = forms.BooleanField(
        label='is_solved'
    )

    def save(self):
        issues_instance = models.Issue_Model()
        issues_instance.title = self.cleaned_data["title"]
        issues_instance.description = self.cleaned_data["description"]
        issues_instance.issue_type = self.cleaned_data["issue_type"]
        issues_instance.date_created = self.cleaned_data["date_created"]
        issues_instance.assigned_user = self.cleaned_data["assigned_user"]
        issues_instance.affected_user = self.cleaned_data["affected_user"]
        issues_instance.is_solved = self.cleaned_data["is_solved"]
        issues_instance.save()
        return issues_instance
