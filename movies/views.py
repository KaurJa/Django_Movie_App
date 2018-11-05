from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os
AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID'),
              'Movies',
              api_key=os.environ.get('AIRTABLE_API_KEY'))


# Create your views here.
# home_page() function runs when you're at youapp.com or redirect from create() function
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request, 'movies/movies_stuff.html', stuff_for_frontend)


def create(request):    # once this function runs , just take me back to home_page.
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/No_image_available_400_x_600.svg/2000px-No_image_available_400_x_600.svg.png'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
                                                # AT.insert(data)adding a movie to database airtable
            response_back_to_user = AT.insert(data) # when new movie is added thats why storing it in a variable to show later in message notification.
            #notify on create
            messages.success(request, "New movie Added {}".format(response_back_to_user['fields'].get('Name'))) # then go to movies_stuff.html to add more

        except Exception as e:
            messages.warning(request, "Got an error when trying to create a new movie {}".format(e))

    return redirect('/')

def edit(request, movie_id):  #movie_id that we are pulling from url.py , now giving access to it in edit function.
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/No_image_available_400_x_600.svg/2000px-No_image_available_400_x_600.svg.png' }] ,
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }
        try:
            response = AT.update(movie_id, data)
            # notify on edit
            messages.success(request, "Updated Movie: {}".format(response['fields'].get('Name')))
        except Exception as e:
            messages.warning(request, "Got an error when trying to update a movie {}".format(e))


    return redirect('/')  # bring back to home page

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        response_deleted = AT.delete(movie_id)
        # notify on delete
        messages.warning(request, "Deleted Movie: {}".format(movie_name))
    except Exception as e:
        messages.warning(request, "Got an error when trying to delete a movie {}".format(e))
    return redirect('/')





