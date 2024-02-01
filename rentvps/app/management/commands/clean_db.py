from django.core.management.base import BaseCommand
from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        TariffVirtual.objects.all().delete()
        Virtual.objects.all().delete()
        Tariff.objects.all().delete()
        CustomUser.objects.all().delete()