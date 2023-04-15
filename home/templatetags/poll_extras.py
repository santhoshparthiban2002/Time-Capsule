from django import template
import datetime
import string
from ..models import *


register = template.Library()

@register.simple_tag
def difference_duration(x):
    delta = x - datetime.date.today()
    beta=delta.days
    return beta

@register.simple_tag
def dates(x):
    return x.strftime("%d-%m-%Y")

@register.simple_tag
def date_time(x):
    return x.strftime("%d-%m-%Y %I:%M:%S %p")


@register.simple_tag
def security_decode(x):
    security = x
    rotate=(security * 3)[len(security) - 7 : 2 * len(security) - 7]
    coded_security=''.join([chr(ord(c)-10) if c in string.printable else c for c in rotate])
    return coded_security




@register.simple_tag
def user_count(x):
    if(x==1):
        profiles=User.objects.all()
        return len(profiles)-1
    elif(x==2):
        profiles=User.objects.filter(delivery__gt=datetime.date.today()).values()
        
        return len(profiles)
    elif(x==3):
        profiles=User.objects.filter(delivery__lte=datetime.date.today()).values()
        return len(profiles)
    elif(x==4):
        profiles=User.objects.all()
        return len(profiles)

@register.simple_tag
def completed_count(x):
    profiles=job.objects.filter(user=x).get()
    return profiles.whatsapp_status

@register.simple_tag
def pending_count(x):
    profiles=job.objects.filter(user=x).get()
    return profiles.whatsapp_status







@register.simple_tag
def model_job_executed(x):
    profiles=job.objects.filter(user=x).get()
    return profiles.executed
@register.simple_tag
def model_job_mail_status(x):
    profiles=job.objects.filter(user=x).get()
    return profiles.mail_status
@register.simple_tag
def model_job_sms_status(x):
    profiles=job.objects.filter(user=x).get()
    return profiles.sms_status
@register.simple_tag
def model_job_whatsapp_status(x):
    profiles=job.objects.filter(user=x).get()
    return profiles.whatsapp_status

