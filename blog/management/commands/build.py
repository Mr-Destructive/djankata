from django.core.management.base import BaseCommand
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def build():
    import os
    os.system("markata build")

class Command(BaseCommand):
    help = "Run Markata build"
    def handle(self,  *args, **kwargs):
        build()
