from django.db import models

from src.domain.common.models import ReadModel


class ProfileLookupByProvider(ReadModel):
  provider_external_id = models.CharField(max_length=2400)
  provider_type = models.CharField(max_length=2400)
  prospect_id = models.CharField(max_length=8)

  class Meta:
    unique_together = ("provider_external_id", "provider_type")

  def __str__(self):
    return 'ProfileLookupByProvider {id}: {provider_type}'.format(id=self.id, provider_type=self.provider_type)
