from django.db import models
from jsonfield import JSONField

from src.domain.common.models import ReadModel


class ActiveTATopicOption(ReadModel):
  option_name = models.CharField(max_length=2400)
  option_type = models.CharField(max_length=2400)
  option_attrs = JSONField()
  ta_topic_id = models.CharField(max_length=8)
  topic_id = models.CharField(max_length=8)
  client_id = models.CharField(max_length=8)

  def __str__(self):
    return 'ActiveTATopicOption {id}: {option_name}'.format(id=self.id, name=self.option_name)
