from __future__ import print_function

import mapbox
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
updater = Updater(token='1134927516:AAE3Bi5dGXbaZWeO_IXIWZjtwMTpzsn6r64') # Токен API к Telegram
dispatcher = updater.dispatcher
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Calendar:
    def __init__(self):
        self.service = None

    def startCommand(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Hello! I am an event manager bot.To use me you have authorise")
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        bot.send_message(chat_id=update.message.chat_id,
                         text="https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=558268665760-efbmhgve4ovnendbv5um6sr5o1shqd4a.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A62799%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.readonly&state=wLSAOuK4H1CvlrgIifQgH9zte1nvcF&access_type=offline")
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

    # def textMessage(bot, update):
    #     response = 'Получил Ваше сообщение: ' + update.message.text
    #     bot.send_message(chat_id=update.message.chat_id, text=response)

    def AddMessage(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="What is the name of event")
        x = update.message.text
        GMT_OFF = '+03:00'
        event = {
            'summary': 'Dinner with friends',
            'start': {'dateTime': '2015-09-18T19:00:00%s' % GMT_OFF},
            'end': {'dateTime': '2015-09-18T22:00:00%s' % GMT_OFF},
            'attendees': [
                {'email': 'friend1@example.com'},
            ],
        }
        self.service.events().insert(calendarId='primary', sendnotification=True, body=event).execute()

    def DeleteMessage(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="What is the name of event")

    def ChangeMessage(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="What is the name of event")

    def CheckDailyMessage(self, bot, update):
        pass

    def CheckNextEventsMessage(self, bot, update):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        bot.send_message(chat_id=update.message.chat_id, text='Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                                   maxResults=10, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            bot.send_message(chat_id=update.message.chat_id, text='No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            bot.send_message(chat_id=update.message.chat_id, text=(start, event['summary']))


    def geoMessage(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="What is your origin?")
        origin = update.message.text
        # time = time.time(20)
        bot.send_message(chat_id=update.message.chat_id,
                         text="What is your destination?")
        destination = update.message.text
        geocoder = mapbox.Geocoder(access_token='sk.eyJ1IjoiZGlhbmthbG9sNCIsImEiOiJjazhzdjE4c3QwMnlwM2Rud2EwZzg1b29iIn0.OqtyNqmiJI5q6UbWQC6oCQ')
        response = geocoder.forward('Paris, France')
        with open('text.json', 'w', encoding='UTF-8') as f:
            json.dump(response.json(), f)

        from mapbox import Directions
        resp = Directions('mapbox.driving').directions([origin, destination])
        driving_routes = resp.geojson()
        first_route = driving_routes['features'][0]
        bot.send_message(chat_id=update.message.chat_id,
                         pic=resp)

if __name__ == "__main__":
    # Хендлеры
    c = Calendar()
    start_command_handler = CommandHandler('start', c.startCommand)
    # text_message_handler = MessageHandler(Filters.text, textMessage)
    geo_message_handler = CommandHandler('root', c.geoMessage)
    add_message_handler = CommandHandler('add', c.AddMessage)
    delete_message_handler = CommandHandler('delete', c.DeleteMessage)
    change_message_handler = CommandHandler('change', c.ChangeMessage)
    check_daily_message_handler = CommandHandler('check_daily', c.CheckDailyMessage)
    check_weekly_message_handler = CommandHandler('check_next_events', c.CheckNextEventsMessage)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    # dispatcher.add_handler(text_message_handler)
    dispatcher.add_handler(geo_message_handler)
    dispatcher.add_handler(add_message_handler)
    dispatcher.add_handler(delete_message_handler)
    dispatcher.add_handler(change_message_handler)
    dispatcher.add_handler(check_daily_message_handler)
    dispatcher.add_handler(check_weekly_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()