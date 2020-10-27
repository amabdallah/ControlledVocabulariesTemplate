import os
import json
import xlrd
from django.db import IntegrityError
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

models_mapping_template = """'%s' : %s,
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

mappings = """models = {
%s
}""" % models_mapping

exec(mappings)

class Command(BaseCommand):
    help = 'Populates the database from an excel file with a given format'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', nargs='+', type=str)

    def handle(self, *args, **options):

        excel_file = options.get('excel_file')

        try:
            wb = xlrd.open_workbook(excel_file[0])
        except IOError as e:
            raise CommandError(e)

        for sheet in wb.sheets():

            # Just get row names
            col_names = []
            for row in range(sheet.nrows):
                if row > 0:
                    break

                if row == 2:
                    continue

                for col in range(sheet.ncols):
                    col_names.append(sheet.cell(row,col).value.lower())

            # Read data from cells
            for row in range(sheet.nrows):
                col_values = []
                if row < 2:
                    continue

                for col in range(sheet.ncols):
                    if isinstance(sheet.cell(row,col).value, float):
                        col_values.append(int(round(sheet.cell(row,col).value)))
                    else:
                        col_values.append(sheet.cell(row,col).value)

                kwargs = dict(zip(col_names, col_values))

                obj = models[sheet.name].objects.filter(term=kwargs['term']).first()

                if not obj:
                    obj = models[sheet.name](**kwargs)
                    obj.save()
                else:
                    print "Avoided duplicate term: %s" % kwargs['term']
