from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_slug

from . import models

# validator to ensure email addresses are unique
def must_be_unique(value):
	user = User.objects.filter(email=value)
	if len(user) > 0:
		raise forms.ValidationError("A user with that email already exists.")

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

	"""
	date_created = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Date Created',
		required=True,
	)
	"""

	"""
	assigned_user = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Assigned User',
		required=False,
		max_length=50
	)
	"""

	# this field will eventually be removed as the affected user will
	# be automatically set to the user who is logged in
	"""
	affected_user = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='Affected User',
		required=True,
		max_length=50,
	)
	"""
	# it's now been removed :D

	"""
	is_solved = forms.BooleanField(
		widget = forms.CheckboxInput(
			attrs={'class':'form-check'}
		),
		label='Is this issue solved?'
	)
	"""

	def save(self, this_user):
		issues_instance = models.Issue_Model()
		issues_instance.title = self.cleaned_data["title"]
		issues_instance.description = self.cleaned_data["description"]
		issues_instance.issue_type = self.cleaned_data["issue_type"]
		#issues_instance.date_created = self.cleaned_data["date_created"]
		#issues_instance.assigned_user = self.cleaned_data["assigned_user"]
		issues_instance.affected_user = this_user
		issues_instance.is_solved = 0
		issues_instance.save()
		return issues_instance

class IssueFilter(forms.Form):
	keyword = forms.CharField(
		widget = forms.TextInput(
			attrs={
				'class': 'form-control',
				'id': 'keyword'
			}
		),
		label='Filter by Keyword',
		required=False,
		max_length=100
	)

	issue_type = forms.IntegerField(
		widget = forms.TextInput(
			attrs={
				'class': 'form-control',
				'id': 'issue_type'
			}
		),
		label='Filter by Issue Type',
		required=False
	)

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(
		label="Email",
		required=True,
		validators=[must_be_unique]
	)

	class Meta:
		model = User
		fields = (
			"username",
			"email",
			"password1",
			"password2"
		)

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class' : 'form-control'})
		self.fields['password1'].widget.attrs.update({'onfocus' : 'display_requirements()'})

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

class ProfileForm(forms.Form):
	user_name = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='User Name',
		required=False,
		max_length=150
	)
	
	email = forms.EmailField(
		label="Email",
		required=False
	)

	bio = forms.CharField(
		widget=forms.Textarea(
			attrs={'class': 'form-control'}
		),
		label='Bio',
		required=False,
		max_length=720
	)

	def save(self,id):
		this_user = User.objects.get(id__exact=id)
		if self.cleaned_data["email"] and self.cleaned_data["email"] != this_user.email:
			this_user.email = self.cleaned_data["email"]
		if self.cleaned_data['user_name']:
			this_user.username = self.cleaned_data["user_name"]
		if self.cleaned_data['bio']:
			this_user.profile.bio = self.cleaned_data["bio"]
		this_user.save()
		return this_user

class ProfileFormNontech(forms.Form):
	user_name = forms.CharField(
		widget = forms.TextInput(
			attrs={'class': 'form-control'}
		),
		label='User Name',
		required=False,
		max_length=150
	)
	
	email = forms.EmailField(
		label="Email",
		required=False
	)

	def save(self,id):
		this_user = User.objects.get(id__exact=id)
		if self.cleaned_data["email"] and self.cleaned_data["email"] != this_user.email:
			this_user.email = self.cleaned_data["email"]
		if self.cleaned_data['user_name']:
			this_user.username = self.cleaned_data["user_name"]
		this_user.save()
		return this_user

class ProfileFilter(forms.Form):
	keyword = forms.CharField(
		widget = forms.TextInput(
			attrs={
				'class': 'form-control font-weight-normal',
				'id': 'keyword'
			}
		),
		label='Filter by Keyword',
		required=False,
		max_length=100
	)

	name = forms.CharField(
		widget = forms.TextInput(
			attrs={
				'class': 'form-control font-weight-normal',
				'id': 'issue_type'
			}
		),
		label='Filter by Name',
		required=False,
		max_length=100
	)
