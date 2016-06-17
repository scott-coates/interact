from django.db import models
from jsonfield import JSONField

from src.apps.relational.models import ReadModel


class TopicLookupForClient(ReadModel):
  snowball_stem = models.CharField(max_length=2400)

class TopicLookupForSearch(ReadModel):
  name = models.CharField(max_length=2400)


class ActiveTaTopicOption(ReadModel):
  option_type = models.CharField(max_length=2400)
  option_attrs = JSONField()
  ta_topic_id = models.CharField(max_length=8)
  topic_id = models.CharField(max_length=8)
  client_id = models.CharField(max_length=8)

  def __str__(self):
    return 'ActiveTaTopicOption {id}: {topic_id}'.format(id=self.id, topic_id=self.topic_id)


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
  topic_ids = JSONField(default=dict)
  profile_id = models.CharField(max_length=8)
  prospect_id = models.CharField(max_length=8)
  provider_type = models.CharField(max_length=2400)

  def __str__(self):
    return 'EOLookupForEa {id}'.format(id=self.id)
