# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import json

from django.db import migrations

from cvservices.utils import upper_splitted, lfirst

from settings.config import BASE_DIR

APP_NAME = 'WATER'
APP_URI = 'http://water.org'
APP_AUTHOR = 'WATER Working Group'

cv_models = {}

try:
    with open(os.path.join(BASE_DIR, 'cv_models.json')) as data_file:
        cv_models = json.load(data_file).get('models')
except IOError:
    print("You need to setup the settings cv_models file (see instructions in README.md file.)")

data_migration_template = """scheme(name='%(lfirst)s', title='%(APP_NAME)s %(uppercase)s Controlled Vocabulary', creator='%(APP_AUTHOR)s',
    description='%(description)s',
    uri='%(APP_URI)s/%(lowercase)s'
    ),"""

output_schemes = """"""

for cv_model in cv_models:
    output_schemes += data_migration_template % {'lowercase': cv_model.get('name').lower(),
     'uppercase': cv_model.get('name'),
     'uppersplitted': upper_splitted(cv_model.get('name')),
     'lfirst' : lfirst(cv_model.get('name')),
     'description' : cv_model.get('description'),
     'APP_URI' : APP_URI,
     'APP_NAME' : APP_NAME,
     'APP_AUTHOR' : APP_AUTHOR
     }

# Four spaces to match identation of the function 'forwards'
final_schemes = """scheme.objects.using(db_alias).bulk_create([
        %s
    ])""" % output_schemes


def forwards(apps, schema_editor):
    namespace = apps.get_model('rdfserializer', 'Namespace')
    node = apps.get_model('rdfserializer', 'Node')
    field_relation = apps.get_model('rdfserializer', 'FieldRelation')
    scheme = apps.get_model('rdfserializer', 'Scheme')

    db_alias = schema_editor.connection.alias

    namespace.objects.using(db_alias).bulk_create([
        namespace(alias='skos', reference='http://www.w3.org/2004/02/skos/core'),
        namespace(alias='odm2', reference='http://vocabulary.odm2.org/ODM2/ODM2Terms'),
        namespace(alias='dc', reference='http://purl.org/dc/elements/1.1/'),
    ])

    node.objects.using(db_alias).bulk_create([
        node(name='prefLabel', namespace_id='skos'),
        node(name='definition', namespace_id='skos'),
        node(name='note', namespace_id='skos'),
        node(name='historyNote', namespace_id='skos'),
        node(name='exactMatch', namespace_id='skos'),
        node(name='category', namespace_id='odm2'),
        node(name='producesResult', namespace_id='odm2'),
        node(name='Concept', namespace_id='skos'),
        node(name='inScheme', namespace_id='skos'),
        node(name='offset1', namespace_id='odm2'),
        node(name='offset2', namespace_id='odm2'),
        node(name='offset3', namespace_id='odm2'),
        node(name='defaultUnit', namespace_id='odm2'),
        node(name='dimensionSymbol', namespace_id='odm2'),
        node(name='dimensionLength', namespace_id='odm2'),
        node(name='dimensionMass', namespace_id='odm2'),
        node(name='dimensionTime', namespace_id='odm2'),
        node(name='dimensionCurrent', namespace_id='odm2'),
        node(name='dimensionTemperature', namespace_id='odm2'),
        node(name='dimensionAmount', namespace_id='odm2'),
        node(name='dimensionLight', namespace_id='odm2'),
    ])

    field_relation.objects.using(db_alias).bulk_create([
        field_relation(field_name='name',
                       node=node.objects.using(db_alias).get(name='prefLabel', namespace_id='skos')),
        field_relation(field_name='definition',
                       node=node.objects.using(db_alias).get(name='definition', namespace_id='skos')),
        field_relation(field_name='note',
                       node=node.objects.using(db_alias).get(name='note', namespace_id='skos')),
        field_relation(field_name='provenance',
                       node=node.objects.using(db_alias).get(name='historyNote', namespace_id='skos')),
        field_relation(field_name='provenance_uri',
                       node=node.objects.using(db_alias).get(name='exactMatch', namespace_id='skos')),
        field_relation(field_name='category',
                       node=node.objects.using(db_alias).get(name='category', namespace_id='odm2')),
        field_relation(field_name='produces_result',
                       node=node.objects.using(db_alias).get(name='producesResult', namespace_id='odm2')),
        field_relation(field_name='term',
                       node=node.objects.using(db_alias).get(name='Concept', namespace_id='skos')),
        field_relation(field_name='offset1',
                       node=node.objects.using(db_alias).get(name='offset1', namespace_id='odm2')),
        field_relation(field_name='offset2',
                       node=node.objects.using(db_alias).get(name='offset2', namespace_id='odm2')),
        field_relation(field_name='offset3',
                       node=node.objects.using(db_alias).get(name='offset3', namespace_id='odm2')),
        field_relation(field_name='default_unit',
                       node=node.objects.using(db_alias).get(name='defaultUnit', namespace_id='odm2')),
        field_relation(field_name='dimension_symbol',
                       node=node.objects.using(db_alias).get(name='dimensionSymbol', namespace_id='odm2')),
        field_relation(field_name='dimension_length',
                       node=node.objects.using(db_alias).get(name='dimensionLength', namespace_id='odm2')),
        field_relation(field_name='dimension_mass',
                       node=node.objects.using(db_alias).get(name='dimensionMass', namespace_id='odm2')),
        field_relation(field_name='dimension_time',
                       node=node.objects.using(db_alias).get(name='dimensionTime', namespace_id='odm2')),
        field_relation(field_name='dimension_current',
                       node=node.objects.using(db_alias).get(name='dimensionCurrent', namespace_id='odm2')),
        field_relation(field_name='dimension_temperature',
                       node=node.objects.using(db_alias).get(name='dimensionTemperature', namespace_id='odm2')),
        field_relation(field_name='dimension_amount',
                       node=node.objects.using(db_alias).get(name='dimensionAmount', namespace_id='odm2')),
        field_relation(field_name='dimension_light',
                       node=node.objects.using(db_alias).get(name='dimensionLight', namespace_id='odm2')),
    ])

    exec(final_schemes)


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ('rdfserializer', 'schema_migration'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            hints={'target_db': 'default'}
        ),
    ]
