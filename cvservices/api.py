import os
import csv
import json
import StringIO
from collections import OrderedDict
from django.http.response import HttpResponse
from tastypie.api import Api
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.utils.mime import build_content_type
from rdfserializer.api import ModelRdfResource

from cvservices.utils import upper_splitted, lfirst

from settings.config import BASE_DIR

cv_models = {}

try:
    with open(os.path.join(BASE_DIR, 'cv_models.json')) as data_file:
        cv_models = json.load(data_file).get('models')
except IOError:
    print("You need to setup the settings cv_models file (see instructions in README.md file.)")
    
model_resource_template = """class %(uppercase)sResource(ModelRdfResource):
    scheme = '%(lfirst)s'

    class Meta(ModelRdfResource.Meta):
        queryset = %(uppercase)s.objects.filter(ModelRdfResource.vocabulary_filter)
        resource_name = '%(lowercase)s'
"""

model_resource_register_template = """v1_api.register(%(uppercase)sResource())
"""

imported_model_template = """%s,
"""

output_resources = """"""
imported_models = """"""
output_register = """"""

for cv_model in cv_models:
    imported_models += imported_model_template % cv_model.get('name')
    output_resources += model_resource_template % {'lowercase': cv_model.get('name').lower(),
     'uppercase': cv_model.get('name'),
     'uppersplitted': upper_splitted(cv_model.get('name')),
     'lfirst': lfirst(cv_model.get('name'))}
    output_register += model_resource_register_template % {'uppercase': cv_model.get('name')}

api_import_template = """from models import (
%s
)""" % imported_models

exec(api_import_template)

class CSVSerializer(Serializer):
    formats = ['csv']
    content_types = {
        'csv': 'text/plain'
    }

    def to_csv(self, data, options=None, writer=None):
        options = options or {}
        data = self.to_simple(data, options)
        excluded_fields = [u'resource_uri']

        raw_data = StringIO.StringIO()
        first = True

        if "meta" in data.keys():
            objects = data.get("objects")

            for value in objects:
                test = {}
                for excluded_field in excluded_fields:
                    del value[excluded_field]
                self.flatten(value, test)

                odict = OrderedDict()
                odict['Term'] = test['term']
                del test['term']
                odict['UnitsName'] = test['name']
                del test['name']
                odict['UnitsTypeCV'] = test['type']
                del test['type']
                odict['UnitsAbbreviation'] = test['abbreviation']
                del test['abbreviation']
                odict['UnitsLink'] = test['link']
                del test['link']

                if first:
                    writer = csv.DictWriter(raw_data, odict.keys())
                    writer.writeheader()
                    writer.writerow(odict)
                    first = False
                else:
                    writer.writerow({k: (v.encode('utf-8') if isinstance(v, int) is not True and isinstance(v, type(
                        None)) is not True else v) for k, v in odict.items()})
        else:
            test = {}
            for excluded_field in excluded_fields:
                del data[excluded_field]
            self.flatten(data, test)
            odict = OrderedDict()
            odict['Term'] = test['term']
            del test['term']
            odict['UnitsName'] = test['name']
            del test['name']
            odict['UnitsTypeCV'] = test['type']
            del test['type']
            odict['UnitsAbbreviation'] = test['abbreviation']
            del test['abbreviation']
            odict['UnitsLink'] = test['link']
            del test['link']

            if first:
                writer = csv.DictWriter(raw_data, odict.keys())
                writer.writeheader()
                writer.writerow(odict)
                first = False
            else:
                writer.writerow(odict)
        CSVContent = raw_data.getvalue()
        return CSVContent

    def flatten(self, data, odict={}):
        if isinstance(data, list):
            for value in data:
                self.flatten(value, odict)
        elif isinstance(data, dict):
            for (key, value) in data.items():
                if not isinstance(value, (dict, list)):
                    odict[key] = value
                else:
                    self.flatten(value, odict)

exec(output_resources)

v1_api = Api(api_name='v1')

exec(output_register)