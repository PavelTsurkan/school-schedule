import os
import django


os.environ.setdefault(key="DJANGO_SETTINGS_MODULE", value="school_schedule.settings")
django.setup()