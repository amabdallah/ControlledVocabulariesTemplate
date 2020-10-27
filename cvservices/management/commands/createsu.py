from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('email', nargs='+', type=str)
        parser.add_argument('passwd', nargs='+', type=str)

    def handle(self, *args, **options):

        username = options.get('username', 'admin')[0]
        email = options.get('email', 'admin@site.com')[0]
        passwd = options.get('passwd', 'admin')[0]
        
        if not User.objects.filter(username=username).exists():
            print('Creating account for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email, username=username, password=passwd)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Provided User already exists')
            
