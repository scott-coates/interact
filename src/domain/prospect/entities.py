from src.domain.common import constants
from src.domain.prospect.events import ProspectCreated1, ProfileAddedToProspect1
from src.libs.common_domain.aggregate_base import AggregateBase


class Prospect(AggregateBase):
  def __init__(self):
    super().__init__()
    self._profiles = []

  @classmethod
  def from_attrs(cls, id, attrs):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    ret_val._raise_event(ProspectCreated1(id, attrs))

    return ret_val

  def add_profile(self, id, provider_external_id, provider_type, attrs):
    if not id:
      raise TypeError("id is required")

    if not provider_external_id:
      raise TypeError("provider_external_id is required")

    if not provider_type:
      raise TypeError("provider_type is required")

    if not attrs:
      raise TypeError("attrs_type is required")
    else:
      attrs = self._clean_attrs(attrs)

    self._raise_event(ProfileAddedToProspect1(id, provider_external_id, provider_type, attrs))

  def _clean_attrs(self, attrs):
    websites = attrs.get(constants.WEBSITES)

    if websites:
      # get unique urls from iterable
      websites = list(set(websites))
      ret_val = dict(attrs, **{constants.WEBSITES: websites})

    else:
      ret_val = attrs

    return ret_val

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.attrs = event.attrs

  def _handle_profile_added_to_prospect_1_event(self, event):
    self._profiles.append(Profile(event.ta_topic_id, event.topic_id))

  def __str__(self):
    return 'Prospect {id}'.format(id=self.id)


class Profile:
  def __init__(self, id, provider_external_id, provider_type, attrs):
    self.id = id
    self.provider_external_id = provider_external_id
    self.provider_type = provider_type
    self.attrs = attrs

  def __str__(self):
    return 'Profile {id}: {provider_external_id}'.format(id=self.id, provider_external_id=self.provider_external_id)
