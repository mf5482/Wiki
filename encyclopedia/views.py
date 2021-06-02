from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
import random

from . import util

markdowner = Markdown()

class entryForm(forms.Form):

    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'name':'title'}))
    body = forms.CharField(widget=forms.Textarea(attrs={'name':'body'}))

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.lower() in list(map(lambda x: x.lower(), util.list_entries())):
            raise forms.ValidationError("Article already exists.")
        return title


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):

    if(request.method=="POST"):
        text=request.POST["body"]
        util.save_entry(title, text)
        return HttpResponseRedirect(reverse('encyclopedia:article', args=[title]))

    html = util.get_entry(title)
    if(html is not None):
        html = markdowner.convert(util.get_entry(title))

    return render(request, "encyclopedia/article.html",
    {
        "title": title,
        "text": html
    })

def search(request): 

    title = request.GET["q"]
    if title.lower() in list(map(lambda x: x.lower(), util.list_entries())):
        return HttpResponseRedirect(reverse('encyclopedia:article', args=[title]))
    else:
        results = []
        for x in util.list_entries():
            if x.lower().find(title.lower()) != -1:
                results.append(x)
        
        return render(request, "encyclopedia/search.html", {
            "results": results
        })

def newEntry(request):

    """ if request.method == 'POST':
        newTitle = request.POST['title']
        newBody = request.POST['body']

        if newTitle.lower() not in list(map(lambda x: x.lower(), util.list_entries())):
            util.save_entry(newTitle, newBody)
            return HttpResponseRedirect(reverse('encyclopedia:article', args=[newTitle]))
            
        else:
            return """
    
    if request.method == 'POST':
        form = entryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse('encyclopedia:article', args=[title]))
        else:
            return render(request, "encyclopedia/newEntry.html", {
                'form': form
            })

    return render(request, "encyclopedia/newEntry.html",{
        'form': entryForm
    })

def editEntry(request, title):

    text = util.get_entry(title)

    return render(request, "encyclopedia/editEntry.html",
    {
        "title":title,
        "text":text
    })

def randomArticle(request):
    title= random.choice(util.list_entries())

    return article(request, title)