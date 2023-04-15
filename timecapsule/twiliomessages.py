from django.conf import settings
from twilio.rest import Client

def sms(information,number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create( body=information,from_="+12184384662",to=number)
    return True,message.sid

def whatsapp(information,number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(from_='whatsapp:+14155238886',body=information,
    to='whatsapp:'+number ) 
    return True,message.sid
    