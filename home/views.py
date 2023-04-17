from django.shortcuts import render,redirect
from django.core.mail import *
from django.core import mail
from timecapsule.twiliomessages import sms,whatsapp
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import*
import datetime
from .models import *
from django.contrib.auth.decorators import login_required
import random,string
from django.utils.timezone import now
from django.contrib.auth.decorators import user_passes_test,login_required



def register(request):
    if request.method == 'POST'  :
        jobs=job()
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        whatsapp = request.POST['whatsapp']
        delivery = request.POST['delivery']
        security = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
        rotate=(security * 3)[len(security) + 7 : 2 * len(security) + 7]
        coded_security=''.join([chr(ord(c)+10) if c in string.printable else c for c in rotate])
        user = User.objects.create_user(username="TC", password=security,email=email,name=name, phone=phone,whatsapp=whatsapp,delivery=delivery,security=coded_security)
        user.username="TC"+delivery.replace("-","")+str(user.id)
        user.save()
        info = information()
        info.user=user
        info.message = request.POST.get('messages')
        info.images = request.FILES.get('image')
        info.videos = request.FILES.get('video')
        info.audios = request.FILES.get('audio')
        info.documents =request.FILES.get('document')
        info.save()
        jobs.executed=False
        jobs.sms_status=False
        jobs.mail_status=False
        jobs.whatsapp_status=False
        jobs.user=user
        jobs.save()
        return render(request,"index.html")
    else:
        return render(request,"index.html")


def login(request):
  if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      user = auth.authenticate(username=username, password=password)
      if user is not None:
        if user.is_authenticated and user.is_superuser==True:
          auth.login(request, user)
          return redirect('index')
        elif user.is_authenticated :
          auth.login(request, user)
          return redirect('timecapsule',username=user.username)
        else:
          return redirect('login')
      else:
          messages.info(request, 'Invalid Username or Password')
          return redirect('login')
  else:
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('login')

def admins(user):
    try:
        return user.is_authenticated and user.is_superuser is True
    except User.DoesNotExist:
        return False

@user_passes_test(admins)
def manager_index(request):
  profiles=User.objects.all()
  profile_info=information.objects.all()
  return render(request, 'manager/index.html',{"profile":profiles,"info":profile_info})  

@user_passes_test(admins)
def manager_profile(request):
  profiles=User.objects.all()
  profile_info=information.objects.all()
  return render(request, 'manager/profile.html',{"profile":profiles,"info":profile_info})  

@user_passes_test(admins)
def manager_users(request):
  profiles=User.objects.all()
  dates=datetime.date.today()
  return render(request, 'manager/users.html',{"profile":profiles,"date":dates})  


@user_passes_test(admins)
def manager_delivery(request):
  profiles=User.objects.filter(delivery__gt=datetime.date.today()).values()
  return render(request, 'manager/delivery.html',{"profile":profiles})  

@user_passes_test(admins)
def manager_delivered(request):
  profiles=User.objects.filter(delivery__lte=datetime.date.today()).values()
  return render(request, 'manager/delivered.html',{"profile":profiles})  


@user_passes_test(admins)
def user_profile(request,username):
  profiles=User.objects.filter(username=username).get()
  profile_info=information.objects.get(user=profiles.id)
  jobs=job.objects.get(user=profiles.id)
  mail_msg=profiles.email
  sms_msg=profiles.phone
  whatsapp_msg=profiles.whatsapp
  status=[]
  print(mail_msg)
  if request.method == 'POST'  :
      message1 = request.POST['header']
      message2 = request.POST['signature']
      status = request.POST.getlist('status')
      print(status)
      if('mail' in status):
        send_mail(message1,message2,"timecapsule1.in@gmail.com",[mail_msg])
      if('sms' in status):
        #message3,message4=sms(message1+" "+message2,sms_msg)
        pass
      if('whatsapp' in status):
        message1,message2=whatsapp(message1+" "+message2,whatsapp_msg )
    
  return render(request, 'manager/profile.html',{"profile":profiles,"info":profile_info,"job":jobs})  

@user_passes_test(admins)
def update_password(request,username):
  profiles=User.objects.filter(username=username).get()
  security = ''.join(random.choices(string.ascii_uppercase +string.digits, k=15))
  profiles.set_password(security)
  rotate=(security * 3)[len(security) + 7 : 2 * len(security) + 7]
  coded_security=''.join([chr(ord(c)+10) if c in string.printable else c for c in rotate])
  profiles.security=coded_security
  profiles.save()
  return redirect('user_profile',username)





@login_required
def timecapsule(request,username):
  user=User.objects.filter(username=username).get()
  info = information.objects.get(user=user.id)
  return render(request, 'timecapsule.html',{'info':info,'user':user})







def send_hello():
    print("helo")
    profiles=User.objects.filter(delivery=now().date())
    connection = mail.get_connection()
    connection.open()
    for x in profiles:
        jobs=job.objects.filter(user=x.id).get()
        jobs.executed=True
        jobs.executed_on=now()
        security = x.security
        rotate=(security * 3)[len(security) - 7 : 2 * len(security) - 7]
        coded_security=''.join([chr(ord(c)-10) if c in string.printable else c for c in rotate])
        mails = EmailMessage("welcome"+x.name ,x.username+"   "+coded_security,"timecapsule1.in@gmail.com",[x.email],connection=connection)
        mails.send()
        jobs.mail_status=True
        jobs.mail_id= mails.message().get('Message-ID')
        #message3,message4=sms("username : "+x.username+" "+"password : " + coded_security,x.phone)
        message1,message2=whatsapp("username : "+x.username+" "+"password : " + coded_security,x.whatsapp )

 #       if message3:
  #        jobs.sms_id=message4
   #       jobs.sms_status=True
        if message1:
          jobs.whatsapp_id=message2
          jobs.whatsapp_status=True
        jobs.save()
    connection.close()   



