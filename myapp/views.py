from django.shortcuts import render, HttpResponse
from django.db.models import Q #allows complex query lookups
from . import models
from . import forms

# Create your views here.
def index(request, page=0):

	context = {
		"title":"ODIT - On Demand IT",
		"info":"A new way to find IT professionals.",
		"how":"How it works: ",
		"desc":"Send in a request --> A registered ODITer who has the skills needed receives the request --> They help out. ",
	}
   
	return render(request, "index.html", context=context)

def submit(request):
	if request.method == "POST":
		form = forms.IssueForm(request.POST)
		if form.is_valid():
			form.save()
			form = forms.IssueForm()
	else:
		form = forms.IssueForm()

	context = {
		"title":"ODIT - Make Request",
		"form":form
	}
	return render(request, "submit.html", context=context)

def viewissues(request):
	if request.method == "POST":
		form = forms.IssueFilter(request.POST)
		if form.is_valid():
			issues_list = models.Issue_Model.objects.all()
			if (form.cleaned_data['keyword']):
				issues_list = issues_list.filter(
					Q(title__contains=form.cleaned_data['keyword']) |
					Q(description__contains=form.cleaned_data['keyword']) |
					Q(assigned_user__contains=form.cleaned_data['keyword']) |
					Q(affected_user__contains=form.cleaned_data['keyword'])
				)
			if (form.cleaned_data['issue_type']):
				issues_list = issues_list.filter(
					Q(issue_type__exact=form.cleaned_data['issue_type'])
				)
		else:
			form = forms.IssueFilter()
			issues_list = models.Issue_Model.objects.all()
	else:
		form = forms.IssueFilter()
		issues_list = models.Issue_Model.objects.all()

	context = {
		"title":"ODIT - View Requests",
		"issues_list":issues_list,
		"form":form,
	}
	return render(request, "viewissues.html", context=context)

def about(request):
	return render(request, "aboutodit.html")