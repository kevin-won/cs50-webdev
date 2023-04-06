from django.shortcuts import render

from . import util

from markdown2 import Markdown

from random import randint

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title, entry):
    mark = Markdown()
    hentry = mark.convert(entry)
    return render(request, "encyclopedia/specificEntry.html", {
            "entry": hentry, "title": title
    })

def entryPage(request, title):
    entry = util.get_entry(title)
    if entry != None:
        return page(request, title, entry)
    else:
        return render(request, "encyclopedia/error.html", {
            "bool": True
        })

def search(request):
    title = request.GET['q']
    entries = util.list_entries()
    if title in entries:
        hentry = util.get_entry(title)
        return page(request, title, hentry)
    else:
        result = []
        for e in entries:
            if title in e:
                result.append(e)
        return render(request, "encyclopedia/index.html", {
        "entries": result
    })

def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    if request.method == "POST":
        title = request.POST['title']
        entry = request.POST['entry']
        entries = util.list_entries()
        if title in entries: 
            return render(request, "encyclopedia/error.html", {
                "bool": False
            })
        else:
            entry = "#" + title + "\n" + entry
            util.save_entry(title, entry)
            entry = util.get_entry(title)
            return page(request, title, entry)
        
def edit(request,title):
    if request.method == "GET":
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "entry": entry, "title": title
        })
    elif request.method == "POST":
        entry = request.POST["entry"]
        util.save_entry(title,entry)
        return page(request, title, entry)

def random(request):
    list = util.list_entries()
    index = randint(0,len(list) - 1)
    title = list[index]
    entry = util.get_entry(title)
    return page(request, title, entry)