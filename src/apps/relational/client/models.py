from django.db import models
from jsonfield import JSONField

from src.apps.relational.models import ReadModel


class TopicLookupForClient(ReadModel):
  snowball_stem = models.CharField(max_length=2400)

class ActiveTATopicOption(ReadModel):
  option_name = models.CharField(max_length=2400)
  option_type = models.CharField(max_length=2400)
  option_attrs = JSONField()
  ta_topic_id = models.CharField(max_length=8)
  topic_id = models.CharField(max_length=8)
  client_id = models.CharField(max_length=8)

  def __str__(self):
    return 'ActiveTATopicOption {id}: {option_name}'.format(id=self.id, option_name=self.option_name)


class ClientLookupForEA(ReadModel):
  ta_attrs = JSONField()
  ta_topics = JSONField(default=list)


class ProspectLookupForEA(ReadModel):
  attrs = JSONField()

  def __str__(self):
    return 'ProspectLookupForEA {id}'.format(id=self.id)


class ProfileLookupForEA(ReadModel):
  profile_attrs = JSONField()
  prospect_id = models.CharField(max_length=8)
  provider_type = models.CharField(max_length=2400)

  def __str__(self):
    return 'ProfileLookupForEA {id}'.format(id=self.id)


class EOLookupForEA(ReadModel):
  eo_attrs = JSONField()
  topic_ids = JSONField(default=list)
  profile_id = models.CharField(max_length=8)
  prospect_id = models.CharField(max_length=8)
  provider_type = models.CharField(max_length=2400)

  def __str__(self):
    return 'EOLookupForEA {id}'.format(id=self.id)
