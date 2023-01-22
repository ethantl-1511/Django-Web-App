# Python Web-Application Internship

## Introduction
During a two-week internship with Prosper IT Consulting, I participated in the creation of a database-driven Django web application using Python. The internship gave me experience using the Agile/Scrum methodology and Azure DevOps. I was given a minimum of 4 stories to complete, and an optional 6 stories to complete over the course of a two week sprint. I completed all 10 with time to spare.
<br><br>
The initial 5 stories had me set up the [back-end CRUD functionality](#crud-stories) for the application and connecting it to my own themed webpage. I styled the various pages using Bootstrap 4 as a base, and CSS for specific style changes. From there, I was given two stories for [implementing an API](#restful-api-stories) into the application, and two stories for [implementing data scrapping with BeautifulSoup](#beautifulsoup-story). Afterward, I had a story to improve the existing UI/UX and add some minor Javascript for flavor. The next story was to add the ability to save a random fact from the API and allow the user to view a list of saved favorites. The final 10th story was free to choose, and I decided to add the ability to delete a selection from the database and reflect it in the list.

Below are further descriptions of the various stories I worked on, along with code snippets of the work. The full code for all of my personal work files are also in this repository, along with a <a href="https://github.com/ethantl-1511/Python-Internship/tree/main/images">folder of images</a> to show visual examples of each section. 

## CRUD Stories
* [Create](#create)
* [Read](#read)
* [Update](#update)
* [Delete](#delete)
* [Etc](#etc)

The basic CRUD functionality for the Django application under the views.py file. 

### Create

      # Function will render the DailyBugle create page when requested
      def dailyBugle_create(request):
        form = PeopleOfInterestForm(data=request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('../create')
        content = {'form': form}
        return render(request, 'DailyBugle/dailyBugle_create.html', content)

### Read

      # Function will render a read/list page from the database
      def dailyBugle_list(request):
          entry = PeopleOfInterest.people.all()
          content = {'entry': entry}
          return render(request, 'DailyBugle/dailyBugle_list.html', content))
          
### Update

      # Function will render update/edit page
      def dailyBugle_edit(request, pk):
          entry = get_object_or_404(PeopleOfInterest, pk=pk)
          form = PeopleOfInterestForm(data=request.POST or None, instance=entry)
          if request.method == 'POST':
              if form.is_valid():
                  form.save()
                  return redirect('../../list')
          content = {'form': form, 'entry': entry}
          return render(request, 'DailyBugle/dailyBugle_edit.html', content)
          
### Delete

      # Function will render delete page
      def dailyBugle_delete(request, pk):
          entry = get_object_or_404(PeopleOfInterest, pk=pk)
          if request.method == 'POST':
              entry.delete()
              return redirect('../../list')
          content = {'entry': entry}
          return render(request, 'DailyBugle/dailyBugle_delete.html', content)
          
### Etc
These functions rendered the home page, and the details page which would be used for the update and delete functions.

      # Function will render DailyBugle page when requested
      def dailyBugle_home(request):
          return render(request, 'DailyBugle/dailyBugle_home.html')

      # Function will render details page
      def dailyBugle_details(request, pk):
          entry = get_object_or_404(PeopleOfInterest, pk=pk)
          content = {'entry': entry}
          return render(request, 'DailyBugle/dailyBugle_details.html', content)

*Jump to: [CRUD Stories](#crud-stories), [Restful API Story](#RESTful-api-stories), [BeautifulSoup Story](#beautifulsoup-story)[Other Skills](#other-skills-learned), [Page Top](#python-internship)*

## RESTful API Stories
* [Create API](#create-api)
* [Save API Results](#save-api-results)
* [Delete Functionality](#delete-functionality)
### Create API
The initial story called for making a request to the API, getting the response, and loading the information. I grabbed three elements to visualize on the relevant webpage.

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

### Save API Results 
A later story called for saving one of the random facts to a list that could be viewed. This code gets the 'random fact' text from the html page, and the 'fact source', then makes a check if the random fact is already in the database and saves it to the database if is not. Additionally, to prevent database duplication errors, I used a try-except to display the page when there is nothing to add.

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

### Delete Functionality
To ensure the saved list could not be cluttered, I created an additional simple delete function specifically for this list. Once again, I used a try-except to prevent errors when the deleted item is removed from the database.
   
      # New delete function for the saved API list
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

*Jump to: [CRUD Stories](#crud-stories), [Restful API Story](#RESTful-api-stories), [BeautifulSoup Story](#beautifulsoup-story)[Other Skills](#other-skills-learned), [Page Top](#python-internship)*

## BeautifulSoup Story
This story involved learning the basics of BeautifulSoup to pull the elements from a website. I used a variable for the url, made a response request, parsed the page using BeautifulSoup and grabbed the content I wanted from a specific sectionof the page, then used regex/split/strip to clean the quote.

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
          
*Jump to: [CRUD Stories](#crud-stories), [Restful API Story](#RESTful-api-stories), [BeautifulSoup Story](#beautifulsoup-story)[Other Skills](#other-skills-learned), [Page Top](#python-internship)*

## Other Skills Learned
- Gained experience with Agile/Scrum methodology, including use of Azure DevOps, daily stand-up meetings, and sprint retrospective.

- Greater understanding of the Django web framework and database-related functionality.

- Gained new experience with APIs, web scrapping, and researching solutions to get them functioning properly.

*Jump to: [CRUD Stories](#crud-stories), [Restful API Story](#RESTful-api-stories), [BeautifulSoup Story](#beautifulsoup-story)[Other Skills](#other-skills-learned), [Page Top](#python-internship)*
