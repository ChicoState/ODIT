from django import forms
from . import models

class IssueForm(forms.Form):
	title = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Title',
		required=True,
		max_length=100
	)

	description = forms.CharField(
		label='Description',
		widget=forms.Textarea(
			attrs={'class': 'form-control'}
		),
		required=False,
		max_length=240
	)

	issue_type = forms.IntegerField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Issue Type',
		required=True
	)

	date_created = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Date Created',
		required=True,
	)

	assigned_user = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Assigned User',
		required=False,
		max_length=50
	)

	affected_user = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Affected User',
		required=True,
		max_length=50,
	)

	is_solved = forms.BooleanField(
		widget = forms.CheckboxInput(
			attrs={'class':'form-check'}
		),
		label='Is this issue solved?'
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

class IssueFilter(forms.Form):
	keyword = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Filter by Keyword',
		required=False,
		max_length=100
	)

	issue_type = forms.IntegerField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Filter by Issue Type',
		required=False
	)