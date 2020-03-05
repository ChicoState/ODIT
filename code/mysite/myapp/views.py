from django.shortcuts import render, HttpResponse
from . import models
from . import forms

# Create your views here.
def index(request, page=0):
    if request.method == "POST":
        form = forms.IssueForm(request.POST)
        if form.is_valid():
            form.save()
            form = forms.IssueForm()
    else:
        form = forms.IssueForm()
    
    issues_list = models.Issue_Model.objects.all()

    context = {
        "title":"ODIT - On Demand IT",
        "info":"A new way to find IT professionals.",
        "how":"How it works: ",
        "desc":"Send in a request --> A registered ODITer who has the skills needed receives the request --> They help out. ",
        "issues_list":issues_list,
        "form":form
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
    
    issues_list = models.Issue_Model.objects.all()

    context = {
        "title":"ODIT - On Demand IT",
        "info":"A new way to find IT professionals.",
        "how":"How it works: ",
        "desc":"Send in a request --> A registered ODITer who has the skills needed receives the request --> They help out. ",
        "issues_list":issues_list,
        "form":form
    }
    return render(request, "submit.html", context=context)

def viewissues(request):
    if request.method == "POST":
        form = forms.IssueForm(request.POST)
        if form.is_valid():
            form.save()
            form = forms.IssueForm()
    else:
        form = forms.IssueForm()
    
    issues_list = models.Issue_Model.objects.all()

    context = {
        "title":"ODIT - On Demand IT",
        "info":"A new way to find IT professionals.",
        "how":"How it works: ",
        "desc":"Send in a request --> A registered ODITer who has the skills needed receives the request --> They help out. ",
        "issues_list":issues_list,
        "form":form
    }
    return render(request, "viewissues.html", context=context)

def about(request):
    return render(request, "aboutodit.html")