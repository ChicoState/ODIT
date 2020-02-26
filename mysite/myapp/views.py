from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    context = {
        "title":"Cody Evans Assignment 3",
        "hello":"CINS465 Hello World",
        #"cup":"{% static "/cup.png" %}"
        "cup":"https://www.we-heart.com/upload-images/dollheadcupsmall.jpg"
    }
    return render(request, "index.html", context=context)
