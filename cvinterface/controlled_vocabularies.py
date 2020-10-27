import os
import json
from cvservices.models import *
from cvinterface.views.base_views import *
from cvservices.utils import upper_splitted, lfirst
from settings.config import BASE_DIR

vocabulary_list_view = DefaultVocabularyListView
vocabulary_detail_view = DefaultVocabularyDetailView
vocabulary_list_template = 'cvinterface/vocabularies/default_list.html'
vocabulary_detail_template = 'cvinterface/vocabularies/default_detail.html'

request_list_view = DefaultRequestListView
request_create_view = DefaultRequestCreateView
request_update_view = DefaultRequestUpdateView
request_list_template = 'cvinterface/requests/default_list.html'
request_create_template = 'cvinterface/requests/default_form.html'
request_update_template = 'cvinterface/requests/default_update_form.html'

cv_models = {}

try:
    with open(os.path.join(BASE_DIR, 'cv_models.json')) as data_file:
        cv_models = json.load(data_file).get('models')
except IOError:
    print("You need to setup the settings cv_models file (see instructions in README.md file.)")

vocabularies_template = """'%(lowercase)s': {
    'name': %(uppercase)s._meta.verbose_name,
    'definition': '%(description)s',
    'model': %(uppercase)s,
},"""

requests_template = """'%(lowercase)srequest': {
    'vocabulary': '%(lowercase)s',
    'vocabulary_model': %(uppercase)s,
    'name': %(uppercase)sRequest._meta.verbose_name,
    'model': %(uppercase)sRequest,
},"""

output_vocabularies = """"""
output_requests = """"""

for cv_model in cv_models:
    output_vocabularies += vocabularies_template % {'lowercase': cv_model.get('name').lower(),
     'uppercase': cv_model.get('name'),
     'uppersplitted': upper_splitted(cv_model.get('name')),
     'description': cv_model.get('description')}
    output_requests += requests_template % {'lowercase': cv_model.get('name').lower(),
     'uppercase': cv_model.get('name'),
     'uppersplitted': upper_splitted(cv_model.get('name'))}

final_vocabularies = """vocabularies = {
    %s
}
""" % output_vocabularies

final_requests = """requests = {
    %s
}
""" % output_requests

exec(final_vocabularies)

exec(final_requests)