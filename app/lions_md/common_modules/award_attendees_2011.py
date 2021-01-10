from collections import defaultdict

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

import orm_settings 
from utilities import get_current_year

d = {'DATABASES': orm_settings.get_db_dict()}

settings.configure(**d)

import models
from django.db.models import Q

class Attendance(object):
    def __init__(self):
        self.lp = False
        self.ls = False
        self.lt = False
        self.total = 0

    def __str__(self):
        return 'LP: %s, LS: %s, LT: %s, Total: %d' % (self.lp, self.ls, self.lt, self.total)

    def __repr__(self):
        return 'LP: %s, LS: %s, LT: %s, Total: %d' % (self.lp, self.ls, self.lt, self.total)

events = []
for e in models.EventAttendance.objects.all().values('event').distinct():
    events.append(e['event'])

events.sort()

for e in events:
    print
    print e
    year = 2012 if 'training' in e else 2012
    d = defaultdict(Attendance)
    for m in models.EventAttendance.objects.filter(event=e):
        d[m.member.club.__unicode__()].total += 1
        club = models.ClubOfficer.objects
        for (name,attr) in (('President','lp'), ('Secretary','ls'), ('Treasurer','lt')):
            off = club.filter(year=year).filter(club=m.member.club).filter(office__title="Club %s" % name)[0]
            if m.member == off.member:
#                print off.member.__unicode__(), name
                setattr(d[m.member.club.__unicode__()],attr,True)
    keys = d.keys()
    keys.sort()
    for k in keys:
        print '%s --> %s' % (k,d[k])
