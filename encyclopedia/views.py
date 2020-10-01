from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .util import list_entries
import random

import markdown2
from django import forms

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_page):
    # Before rendering the entry in HTML, it needs to be converted from Markdown
    entry_page_md = util.get_entry(entry_page)
    if entry_page_md:
        converted_entry = markdown2.markdown(entry_page_md)
    else:
        return render(request, 'encyclopedia/error.html', status=404)

    context = {
        'entry_title': entry_page,
        'entry_text': converted_entry
    }

    return render(request, "encyclopedia/entry.html", context)


def search(request):
    # loop through each item in util.list_entries() and make them lowercase to compare to query
    lower_list = [entry.lower() for entry in util.list_entries()]
    # now that both the query and entries are lowercase, searches are case insensitive and will redirect to the page is available
    if request.GET['q'].lower() in lower_list:
        return redirect('entry_page', entry_page=request.GET['q'])
    else:
        # if an exact match for the query isn't found, return a list of items that partially contain that query
        context = {
            'results': util.search_entries(request.GET['q'])
        }
        return render(request, 'encyclopedia/search.html', context)


def newpage(request):

    if request.method == 'POST':

        entry_title = request.POST.get('entryTitle', 'No Data')
        body_text = request.POST.get('bodyText', 'No Data')

        if len(entry_title) != 0:

            if entry_title not in list_entries():
                util.save_entry(
                    entry_title, (f"# {entry_title}\n\n{body_text}"))

                # return entry(request, entry_title) - apparently HttpResponseRedirect is the cleaner, best practice method
                return HttpResponseRedirect(reverse('entry_page', kwargs={
                    'entry_page': entry_title}))

            else:
                return render(request, 'encyclopedia/error_title.html', status=404)
        else:
            return render(request, 'encyclopedia/error_notitle.html', status=404)

    else:
        return render(request, "encyclopedia/newpage.html")


def editpage(request, entry_page):

    if request.method == "POST":
        text = request.POST.get('editText', 'No Data')
    
        util.save_entry(entry_page, (f"{text}"))

        return HttpResponseRedirect(reverse('entry_page', kwargs={
                    'entry_page': entry_page}))

    else:                 
        entry_page_md = util.get_entry(entry_page)

        context = {
            'entry_text': entry_page_md
        }

        return render(request, "encyclopedia/editpage.html", context)
    
def randompage(request):
    # using python's random module, we can select a random element from a list
    randomPage = random.choice(util.list_entries())
   
    return redirect('entry_page', entry_page=randomPage)
    # return HttpResponseRedirect(reverse('entry_page', kwargs={
    #                 'entry_page': randomPage}))