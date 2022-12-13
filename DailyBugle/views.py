from django.shortcuts import render, redirect, get_object_or_404
from .forms import PeopleOfInterestForm, RandomFactForm
from .models import PeopleOfInterest, RandomFact
import requests
import json
from bs4 import BeautifulSoup
import re

# Function will render DailyBugle page when requested
def dailyBugle_home(request):
    return render(request, 'DailyBugle/dailyBugle_home.html')

# Function will render the DailyBugle create page when requested
def dailyBugle_create(request):
    form = PeopleOfInterestForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('../create')
    content = {'form': form}
    return render(request, 'DailyBugle/dailyBugle_create.html', content)

# Function will render a list from the database
def dailyBugle_list(request):
    entry = PeopleOfInterest.people.all()
    content = {'entry': entry}
    return render(request, 'DailyBugle/dailyBugle_list.html', content)

# Function will render details page
def dailyBugle_details(request, pk):
    entry = get_object_or_404(PeopleOfInterest, pk=pk)
    content = {'entry': entry}
    return render(request, 'DailyBugle/dailyBugle_details.html', content)

# Function will render edit page
def dailyBugle_edit(request, pk):
    entry = get_object_or_404(PeopleOfInterest, pk=pk)
    form = PeopleOfInterestForm(data=request.POST or None, instance=entry)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('../../list')
    content = {'form': form, 'entry': entry}
    return render(request, 'DailyBugle/dailyBugle_edit.html', content)

# Function will render delete page
def dailyBugle_delete(request, pk):
    entry = get_object_or_404(PeopleOfInterest, pk=pk)
    if request.method == 'POST':
        entry.delete()
        return redirect('../../list')
    content = {'entry': entry}
    return render(request, 'DailyBugle/dailyBugle_delete.html', content)

# Function for API
def dailyBugle_api(request):
    url = 'https://uselessfacts.jsph.pl/random.json?language=en'
    response = requests.request("GET",url)
    #print(response) # should return "<Response [200]> to the terminal
    api_info = json.loads(response.text)

    # These variables get text, source, and source_url from the API dictionary
    api_text = api_info.get('text')
    api_source = api_info.get('source')
    api_source_url = api_info.get('source_url')

    content = { "api_text":api_text, "api_source":api_source, "api_source_url":api_source_url }
    return render(request, 'DailyBugle/dailyBugle_api.html', content)

# Function for Beautiful Soup
def dailyBugle_bs(request):
    url = 'https://marvel.fandom.com/wiki/John_Jonah_Jameson_(Earth-616)'
    response = requests.request("GET",url)
    #print(response)  # should return "<Response [200]> to the terminal

    source = BeautifulSoup(response.content, 'html.parser')
    # Grabbing a specific area of the site's HTML that houses a quote I want, selecting the HTML tags
    bs_quote = str(source.select('dd i'))

    # Using regex to remove the HTML tags from the string
    reg_quote = re.sub(re.compile('<.*?>'), '', bs_quote)
    # Split to remove brackets, strip to remove extra space
    clean_quote = reg_quote.split("]")[0].split("[")[1].strip()
    #print(clean_quote)
    content = { 'clean_quote': clean_quote }
    return render(request, 'DailyBugle/dailyBugle_bs.html', content)

# Functions to view RandomFact database as a list
def dailyBugle_favoriteAPI(request):
    # Try to get API parts to save from API.html
    try:
        api_text = request.GET['random_fact']
        api_source = request.GET['fact_source']

        # Block to check if 'random_fact' already exists in database
        # If not found, save.
        found = False
        for a in RandomFact.facts.all():
            if (str(a) == str(api_text)):
                found = True
                break
        if not found:
            entry = RandomFact(
                random_fact=api_text,
                fact_source=api_source,
            )
            entry.save()
    except: # If it fails to get...
        print("Could not get sources and save to database. Displaying list.")

    # Display list
    entry = RandomFact.facts.all()
    content = {'entry': entry}
    return render(request, 'DailyBugle/dailyBugle_favoriteAPI.html', content)

def dailyBugle_deleteAPI(request, id):
    try:
        saved = RandomFact.facts.get(id=id)
        saved.delete()
    except:
        print("Nothing to delete.")

    # Display list
    entry = RandomFact.facts.all()
    content = {'entry': entry}
    return render(request, 'DailyBugle/dailyBugle_favoriteAPI.html', content)