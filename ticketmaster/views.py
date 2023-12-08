from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
import requests
from datetime import datetime
from django.contrib import messages
import time
from .models import SearchInput
from .models import EventTable
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Adrian + Sheel: Created response in views.py
# Adrian: GET and POST
def post_events(request):
    if request.method == 'POST':
        search = request.POST['search']
        location = request.POST['location']

        if not search:
            messages.info(request, 'Search term cannot be empty. Please enter a search term.')
            return redirect('ticketmaster-results')
        elif not location:
            messages.info(request, 'Location term cannot be empty. Please enter a location term.')
            return redirect('ticketmaster-results')
        else:
            search_input = SearchInput(search=search, location=location)
            search_input.save()
            print("Search saved!")

        event_results = get_events(search, location)

        if event_results is None:
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            return redirect('ticketmaster-results')
        else:
            events = event_results.get("_embedded", {}).get("events", [])

            if not events:
                messages.info(request, 'No events found for the given search and location.')
                return render(request, 'results.html')

            event_list = []
            id = 1

            for event in events:
                event_id = id
                event_image = event["images"][0]["url"]
                event_name = event["name"]
                venue = event["_embedded"]["venues"][0]
                venue_name = venue["name"]
                city_name = venue["city"]["name"]
                state_name = venue["state"]["stateCode"]
                address_line = venue["address"]["line1"]
                ticket_url = event["url"]
                try:
                    event_date_and_time = event["dates"]["start"]["dateTime"]
                except KeyError:
                    event_date_and_time = "N/A"

                if event_date_and_time == "N/A":
                    event_date = "N/A"
                    event_date_fix = "N/A"
                    event_time = "N/A"
                    event_time_fix = "N/A"
                else:
                    event_date = datetime.strptime(event_date_and_time[:10], "%Y-%m-%d")
                    event_date_fix = event_date.strftime("%a %b %d %Y")
                    event_time = datetime.strptime(event_date_and_time[11:16], "%H:%M")
                    event_time_fix = event_time.strftime("%I:%M %p")

                event_details = {
                    'event_id': event_id,
                    'event_image': event_image,
                    'event_name': event_name,
                    'venue_name': venue_name,
                    'city_name': city_name,
                    'state_name': state_name,
                    'address_line': address_line,
                    'ticket_url': ticket_url,
                    'event_date': event_date_fix,
                    'event_time': event_time_fix
                }

                event_list.append(event_details)
                id = event_id + 1

            context = {'events': event_list}
            return render(request, 'results.html', context)

    return render(request, 'results.html')


def get_events(search, location):
    try:
        url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=GIw7Q68q75qxP3Tp7eV1QFNtSeGP1Dnf"
        params = {
            "classificationName": search,
            "city": location,
            "sort": "date,asc"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


# Adrian: CRUD Operations
@csrf_exempt
def create_bookmark(request):
    if request.method == 'POST':
        event_receive = json.loads(request.body.decode('utf-8'))
        bookmark_image = event_receive.get('eventImage')
        bookmark_name = event_receive.get('eventName')
        bookmark_location = event_receive.get('eventLocation')
        bookmark_date = event_receive.get('eventDate')
        bookmark_time = event_receive.get('eventTime')
        bookmark_url = event_receive.get('ticketURL')

        # Let Django manage the 'id' field automatically
        event = EventTable.objects.create(
            eventImage=bookmark_image,
            eventName=bookmark_name,
            eventLocation=bookmark_location,
            eventDate=bookmark_date,
            eventTime=bookmark_time,
            eventTicketURL=bookmark_url,
            favorite=False
        )

    return redirect('ticketmaster-bookmarks')


# To test stuff WITHOUT the login, comment out the @login_required line below.
@login_required(login_url='/login/')
def view_bookmarks(request):
    bookmark_events = EventTable.objects.all()
    context = {'events': bookmark_events}
    print(context)
    return render(request, 'eventsave.html', context)


@csrf_exempt
def update_bookmark(request):
    if request.method == 'POST':
        event_receive_id = json.loads(request.body.decode('utf-8'))
        event_id = event_receive_id.get('eventId')

    bookmark_event = EventTable.objects.get(id=event_id)

    if bookmark_event.favorite is False:
        bookmark_event.favorite = True
    elif bookmark_event.favorite is True:
        bookmark_event.favorite = False
    bookmark_event.save()

    return redirect('ticketmaster-bookmarks')


@csrf_exempt
def delete_bookmark(request):
    if request.method == 'POST':
        event_receive_id = json.loads(request.body.decode('utf-8'))
        event_id = event_receive_id.get('eventId')

    bookmark_event = EventTable.objects.get(id=event_id)
    bookmark_event.delete()
    return redirect('ticketmaster-bookmarks')


# Adrian: User operations
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticketmaster-bookmarks')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ticketmaster-bookmarks')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('ticketmaster-bookmarks')
