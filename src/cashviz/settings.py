# Project specific settings
from datetime import date

from django.apps import AppConfig

from config import HELL_CONFIG


class CashvizConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cashviz"


ALLOWED_HOSTS = HELL_CONFIG.allowed_hosts

NO_FEE_2019 = True
HELL_START_DATE = date(2021, 5, 1)
FEE_START_DATE = date(2020, 1, 1)
