from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
from pathlib import Path

class Command(BaseCommand):
    help = 'Extract translation strings from code and templates'

    def handle(self, *args, **options):
        # Get the base directory
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        locale_dir = base_dir / 'locale'
        
        # Create locale directory if it doesn't exist
        if not locale_dir.exists():
            locale_dir.mkdir()
            self.stdout.write(f'Created locale directory at {locale_dir}')
        
        # Extract messages from Python files and templates
        self.stdout.write('Extracting translation strings...')
        try:
            call_command('makemessages', '--all', '--keep-pot', '--no-wrap',
                        '--ignore=venv/*', '--ignore=node_modules/*',
                        '--ignore=.git/*', '--ignore=static/*',
                        '--no-location')
            
            self.stdout.write(
                self.style.SUCCESS('Successfully extracted translation strings')
            )
            
            # Give instructions for translation
            self.stdout.write('\nNext steps:')
            self.stdout.write('1. Edit the .po files in the locale directory')
            self.stdout.write('2. Run `python manage.py compilemessages` to compile the translations')
            
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Error extracting translation strings: {e}')
            )
