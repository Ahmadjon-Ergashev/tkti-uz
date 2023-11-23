import os
import django
import random
from collections import namedtuple
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local_settings")
django.setup()

from main.models import news  

# for i in range(3):
#     print(str(random.randint(111111, 999999)))


events = news.Events.objects.all()
print(events[0:1])
