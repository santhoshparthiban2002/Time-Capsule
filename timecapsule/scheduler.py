from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from django_apscheduler.jobstores import register_events, DjangoJobStore
from home.views import send_hello
import datetime

def start():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', seconds=10, id='auto_hello', name='auto_hello')
    #@scheduler.scheduled_job('cron', hour=21, id='auto_hello', name='auto_hello')
    def auto_hello():
        execution = DjangoJobExecution(
            job=DjangoJob.objects.get(id='auto_hello'),
            run_time=timezone.now(),
        )
        execution.save()
  

    job = DjangoJob(
        id='auto_hello',
        next_run_time=datetime.datetime.now(),
        
    )
    job.save()
    scheduler.add_job(auto_hello)
    scheduler.start()
