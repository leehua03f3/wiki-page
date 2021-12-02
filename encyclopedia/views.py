from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from random import randrange

from . import util
from markdown2 import Markdown

markdowner = Markdown()

# class SearchForm(forms.Form):
# 	search = forms.CharField(label='Search Encyclopedia', max_length=100)

def index(request):
    return render(request, "encyclopedia/index.html", {
    	"entries": util.list_entries()
    	})

def entry(request, name):
	error = "404 not found"
	entries = util.list_entries()
	same_case_entries = []
	for entry in entries:
		same_case_entries.append(entry.lower())

	if name.lower() not in same_case_entries:
		return render(request, "encyclopedia/error.html", {"error": error})
	else:
		entry_content = markdowner.convert(util.get_entry(name))
		return render(request,  "encyclopedia/entry.html", {
				"name": name,
				"entry_content": entry_content
			})

def search(request):
	entries = util.list_entries()
	search_input = request.POST.get("q")
	same_case_entries = []

	for entry in entries:
		same_case_entries.append(entry.lower())

	if search_input.lower() in same_case_entries:
		return HttpResponseRedirect(reverse("entry", args=[search_input]))
	else:
		results = []
		for entry in entries:
			lower_entry = entry.lower()
			lower_input = search_input.lower()
			for index in range(1, len(lower_entry)):
				if lower_entry[0:index] == lower_input:
					results.append(entry)
		return render(request, "encyclopedia/results.html", {
			"results": results
			})

def newpage(request): 
	if request.method == "POST":
		title = request.POST.get("title")
		same_case_entries = []

		for entry in util.list_entries():
			same_case_entries.append(entry.lower())

		error = "Duplicate title"
		if title.lower() in same_case_entries:
			return render(request, "encyclopedia/error.html", {"error": error})

		content = request.POST.get("content")
		util.save_entry(title, content)
		entries = util.list_entries()
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "encyclopedia/newpage.html")

def randomPage(request):
	entries = util.list_entries()
	rand_num = randrange(0, len(entries) - 1)
	rand_page = entries[rand_num]
	entry_content = markdowner.convert(util.get_entry(rand_page))
	return render(request,  "encyclopedia/entry.html", {
			"name": rand_page,
			"entry_content": entry_content
		})

def editpage(request):
	if request.method == "POST":
		title = request.POST.get("title")
		content = request.POST.get("content")
		util.save_entry(title, content)
		return HttpResponseRedirect(reverse("index"))
		# return HttpResponseRedirect(reverse(title))
	else:
		title = request.GET.get("title")
		content = util.get_entry(title)
		return render(request, "encyclopedia/editpage.html", {
				"title": title,
				"content": content
			})

	# TODO: