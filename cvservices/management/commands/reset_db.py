import os
import json
from django.core.management.base import BaseCommand, CommandError

from settings.config import BASE_DIR

cv_models = {}

try:
    with open(os.path.join(BASE_DIR, 'cv_models.json')) as data_file:
        cv_models = json.load(data_file).get('models')
except IOError:
    print("You need to setup the settings cv_models file (see instructions in README.md file.)")
    
imported_model_template = """%s,
"""

models_mapping_template = """for object in %s.objects.all():
    object.delete()
"""

imported_models = """"""
models_mapping = """"""

for cv_model in cv_models:
    imported_models += imported_model_template % cv_model.get('name')
    models_mapping += models_mapping_template % cv_model.get('name')

api_import_template = """from cvservices.models import (
%s
)""" % imported_models

exec(api_import_template)

class Command(BaseCommand):
    help = 'Deletes every model object in the database'

    def handle(self, *args, **options):

        exec(models_mapping)