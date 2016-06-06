from django.db import models
from jsonfield import JSONField

from src.domain.common.models import ReadModel


class ActiveTATopic(ReadModel):
  options = JSONField()
  topic_id = models.CharField(max_length=8)
  client_id = models.CharField(max_length=8)

  def __str__(self):
    return 'ActiveTATopic {id}: {name}'.format(id=self.id, name=self.name)
