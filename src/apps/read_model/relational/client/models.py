from django.db import models
from jsonfield import JSONField

from src.apps.read_model.relational.models import ReadModel


class ActiveTaTopicOption(ReadModel):
  option_name = models.CharField(max_length=2400)
  option_type = models.CharField(max_length=2400)
  option_attrs = JSONField()
  ta_topic_id = models.CharField(max_length=8)
  ta_topic_relevance = models.PositiveSmallIntegerField()
  topic_id = models.CharField(max_length=8)
  client_id = models.CharField(max_length=8)

  def __str__(self):
    return 'ActiveTaTopicOption {id}: {option_name}'.format(id=self.id, option_name=self.option_name)


class ClientLookupForEa(ReadModel):
  ta_attrs = JSONField()
  ta_topics = JSONField(default=dict)


class ProspectLookupForEa(ReadModel):
  attrs = JSONField()
  topic_ids = JSONField(default=list)

  def __str__(self):
    return 'ProspectLookupForEa {id}'.format(id=self.id)


class ProfileLookupForEa(ReadModel):
  profile_attrs = JSONField()
  prospect_id = models.CharField(max_length=8)
  provider_type = models.CharField(max_length=2400)

  def __str__(self):
    return 'ProfileLookupForEa {id}'.format(id=self.id)


class EoLookupForEa(ReadModel):
  eo_attrs = JSONField()
  topic_ids = JSONField()
  provider_type = models.CharField(max_length=2400)
  profile_id = models.CharField(max_length=8)
  prospect_id = models.CharField(max_length=8)

  def __str__(self):
    return 'EoLookupForEa {id}'.format(id=self.id)


class BatchEa(ReadModel):
  attrs = JSONField()
  score_attrs = JSONField()
  client_id = models.CharField(max_length=8)
  batch_id = models.CharField(max_length=8)
  counter = models.PositiveIntegerField()
  prospect_id = models.CharField(max_length=8)

  def __str__(self):
    return 'BatchEa {id}'.format(id=self.id)


class DeliveredEa(ReadModel):
  name = models.CharField(max_length=2400)
  bio = models.TextField()
  location = models.CharField(max_length=2400)
  url = models.CharField(max_length=2400)
  score = models.DecimalField(max_digits=19, decimal_places=7)
  score_attrs = JSONField()
  assigned_entities = JSONField()
  prospect_id = models.CharField(max_length=8)

  def __str__(self):
    return 'DeliveredEa {id}'.format(id=self.id)
