from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from django.db import models

import os
import json

from cvservices.utils import upper_splitted, lfirst

from settings.config import BASE_DIR

class ControlledVocabulary(models.Model):
    CURRENT = 'Current'
    ARCHIVED = 'Archived'

    STATUS_CHOICES = (
        (CURRENT, 'Current'),
        (ARCHIVED, 'Archived')
    )

    vocabulary_id = models.AutoField(primary_key=True)
    term = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    definition = models.TextField()
    category = models.CharField(max_length=255, blank=True)
    provenance = models.TextField(blank=True)
    provenance_uri = models.URLField(db_column='provenanceUri', blank=True)
    note = models.TextField(blank=True, null=True)
    vocabulary_status = models.CharField(max_length=255, db_column='status', choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    previous_version = models.OneToOneField('self', null=True, related_name='revised_version')

    def has_revision(self):
        revision = None
        try:
            revision = self.revised_version
        except ObjectDoesNotExist:
            pass
        return revision is not None

    def get_latest_version(self):
        term = self
        while term.has_revision():
            term = term.revised_version
        return term

    class Meta:
        db_table = 'controlledvocabularies'
        ordering = ["-name"]


class ControlledVocabularyRequest(models.Model):
    PENDING = 'Pending'
    REJECTED = 'Rejected'
    ACCEPTED = 'Accepted'
    ARCHIVED = 'Archived'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (ACCEPTED, 'Accepted'),
        (ARCHIVED, 'Archived'),
    )

    request_id = models.AutoField(max_length=255, db_column='requestId', primary_key=True)

    term = models.CharField(max_length=255, help_text="Please enter a URI-friendly version of your term with no spaces, special characters, etc.")
    name = models.CharField(max_length=255, help_text="Please enter the term as you would expect it to appear in a sentence.")
    definition = models.TextField(help_text="Please enter a detailed definition of the term.", blank=True)
    category = models.CharField(max_length=255, blank=True, help_text="You may suggest a category for the term. Refer to the vocabulary to see which categories have been used. You may also suggest a new category.")
    provenance = models.TextField(blank=True, help_text="Enter a note about where the term came from. If you retrieved the definition of the term from a website or other source, note that here.")
    provenance_uri = models.URLField(db_column='provenanceUri', blank=True, max_length=1024, help_text="If you retrieved the term from another formal vocabulary system, enter the URI of the term from the other system here.")
    note = models.TextField(blank=True, null=True, help_text="Please enter any additional notes you may have about the term.")

    status = models.CharField(max_length=255, db_column='status', choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    date_submitted = models.DateField(db_column='dateSubmitted', default=timezone.now)
    date_status_changed = models.DateField(db_column='dateStatusChanged', default=timezone.now)
    request_notes = models.TextField(db_column='requestNotes', blank=True)
    submitter_name = models.CharField(max_length=255, db_column='submitterName', help_text="Enter your name.")
    submitter_email = models.CharField(max_length=255, db_column='submitterEmail', help_text="Enter your email address.")
    request_reason = models.TextField(db_column='requestReason', help_text="Please enter a brief description of the reason for your submission (e.g., Term does not exist yet, Term is needed for my data use case, etc.)")

    request_for = models.ForeignKey('ControlledVocabulary', db_column='requestFor', blank=True, null=True)
    original_request = models.ForeignKey('self', db_column='originalRequestId', null=True)

    class Meta:
        db_table = 'requests'
        ordering = ["date_submitted", "-request_id"]

cv_models = {}

try:
    with open(os.path.join(BASE_DIR, 'cv_models.json')) as data_file:
        cv_models = json.load(data_file).get('models')
except IOError:
    print("You need to setup the settings cv_models file (see instructions in README.md file.)")
    
model_template = """class %(uppercase)s(ControlledVocabulary):
    class Meta:
        db_table = '%(lowercase)s'
        verbose_name = '%(uppercase)s'
        ordering = ["name"]
class %(uppercase)sRequest(ControlledVocabularyRequest):
    class Meta:
        db_table = '%(lowercase)srequests'
        verbose_name = '%(uppersplitted)s Request'
"""

output_models = """"""

for cv_model in cv_models:
    output_models += model_template % {'lowercase': cv_model.get('name').lower(),
     'uppercase': cv_model.get('name'),
     'uppersplitted': upper_splitted(cv_model.get('name'))}

exec(output_models)