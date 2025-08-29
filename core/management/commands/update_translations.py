import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Update and compile translation files for all languages'

    def handle(self, *args, **options):
        # Create locale directory if it doesn't exist
        os.makedirs(os.path.join(settings.BASE_DIR, 'locale'), exist_ok=True)
        
        # Extract messages for all languages
        self.stdout.write('Extracting messages...')
        os.system('django-admin makemessages -l en -l ne --ignore=venv/* --ignore=static/* --ignore=media/*')
        
        # Compile messages
        self.stdout.write('Compiling messages...')
        os.system('django-admin compilemessages')
        
        self.stdout.write(self.style.SUCCESS('Successfully updated translations'))
