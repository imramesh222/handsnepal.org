from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Compile translation files (.po to .mo)'

    def handle(self, *args, **options):
        self.stdout.write('Compiling translation files...')
        try:
            call_command('compilemessages')
            self.stdout.write(
                self.style.SUCCESS('Successfully compiled translation files')
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f'Error compiling translation files: {e}')
            )
