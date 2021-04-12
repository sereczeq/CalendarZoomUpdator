from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.

SCOPES = ['https://www.googleapis.com/auth/calendar']

paradigms_link = "https://pwr-edu.zoom.us/j/98732547803?pwd=MjFRbnYrZVMzYzY0NVF1aWVUNUQ2Zz09"

class Calendar_Updator:
    def __init__(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def edit_events(self, data):

        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(
                calendarId='classroom115865766386493347802@group.calendar.google.com', timeMin=now,
                maxResults=20, singleEvents=True,
                orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:

            # programming paradigms has static link
            if "W Programming paradigms" in event["summary"]:
                description = event["description"]
                # if the link is not there already
                if "https://" not in description:
                    updated_event = self.service.events().update(
                            calendarId='classroom115865766386493347802@group.calendar.google.com',
                            eventId=event['id'],
                            body={
                                "summary": event["summary"],
                                "description": description + "\n" + paradigms_link,
                                "start": event["start"],
                                "end": event["end"],
                                },
                            ).execute()
                    print("updated: ", updated_event['summary'])
                continue

            # normal search
            found = False
            for tup in data:
                # check for every type of date (some have +/- 1 minute)
                if any(date in str(event['start']) for date in tup):
                    found = True
                    description = event["description"]
                    # if the link is not there already
                    if "https://" not in description:
                        updated_event = self.service.events().update(
                                calendarId='classroom115865766386493347802@group.calendar.google.com',
                                eventId=event['id'],
                                body={
                                    "summary": event["summary"],
                                    "description": description + "\n" + tup[-1],
                                    "start": event["start"],
                                    "end": event["end"],
                                    },
                                ).execute()
                        print("updated: ", updated_event['summary'])
                    else:
                        print("found but didn't update, because", description)
                    break
            if not found:
                print("didn't find date for: ", event['summary'], event['start'])
