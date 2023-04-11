import os
from celery.app.base import Celery as CeleryClass
from celery.schedules import crontab
from celery import Celery
from .LIST_AM import list_am_main_cycle
from .LALAFO import lalafo_main_cycle
from .KUFAR import kufar_main_cycle
from .KOLESA_KZ import kolesa_kz_main_cycle
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aurMain.settings')

app = Celery('PARSING')
# app.conf.timezone = 'UTC'
app.conf.timezone = 'Europe/Moscow'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task()
def list_am():
    list_am_main_cycle()
    return 'COMPLITTED'


@app.task()
def lalafo():
    lalafo_main_cycle()
    return 'COMPLITTED'


@app.task()
def kufar():
    kufar_main_cycle()
    return 'COMPLITTED'


@app.task()
def kolesa_kz():
    import time
    stat = time.time()
    kolesa_kz_main_cycle()
    finish = time.time()
    f = open('timing.txt', 'w')
    f.write(f'start time: {stat}\nfinish time: {finish}\nworking time: {str(finish-stat)}')
    return 'COMPLITTED'


@app.on_after_configure.connect
def setup_periodic_tasks(sender: CeleryClass, **kwargs):
    # kufar.delay()
    # lalafo.delay()
    # list_am.delay()
    kolesa_kz.delay()
    sender.add_periodic_task(
        crontab(minute=1, hour='*'),
        list_am.s(),
        start_time=datetime.datetime.now(),
        name='LIST.AM',

    )
    sender.add_periodic_task(
        crontab(minute=20, hour='*'),
        lalafo.s(),
        start_time=datetime.datetime.now(),
        name='LALAFO',

    )
    sender.add_periodic_task(
        crontab(minute=40, hour='*'),
        kufar.s(),
        start_time=datetime.datetime.now(),
        name='KUFAR',
    )
