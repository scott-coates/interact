from django.db import models
from jsonfield import JSONField

from src.apps.relational.models import ReadModel


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

  def __str__(self):
    return 'ProspectLookupForEa {id}'.format(id=self.id)


class ProfileLookupForEa(ReadModel):
  profile_attrs = JSONField()
  prospect_id = models.CharField(max_length=8)
  provider_type = models.CharField(max_length=2400)

  def __str__(self):
    return 'ProfileLookupForEa {id}'.format(id=self.id)


class EOLookupForEa(ReadModel):
  eo_attrs = JSONField()
  profile_id = models.CharField(max_length=8)
  prospect_id = models.CharField(max_length=8)
  provider_type = models.CharField(max_length=2400)

  def __str__(self):
    return 'EOLookupForEa {id}'.format(id=self.id)
