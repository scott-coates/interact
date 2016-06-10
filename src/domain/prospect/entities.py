from src.domain.prospect.events import ProspectCreated1, ProfileAddedToProspect1
from src.domain.prospect.profile import service as profile_service
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

  def add_profile(self, id, profile_external_id, provider_type, _profile_service=None):
    if not _profile_service: _profile_service = profile_service
    if not id:
      raise TypeError("id is required")

    if not profile_external_id:
      raise TypeError("profile_external_id is required")

    if not provider_type:
      raise TypeError("provider_type is required")

    attrs = _profile_service.get_profile_attrs_from_provider(profile_external_id, provider_type)

    self._raise_event(ProfileAddedToProspect1(id, profile_external_id, provider_type, attrs))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.attrs = event.attrs

  def _handle_profile_added_to_prospect_1_event(self, event):
    self._profiles.append(Profile(**event.data))

  def __str__(self):
    return 'Prospect {id}'.format(id=self.id)


class Profile:
  def __init__(self, id, profile_external_id, provider_type, attrs):
    self.id = id
    self.profile_external_id = profile_external_id
    self.provider_type = provider_type
    self.attrs = attrs

  def __str__(self):
    return 'Profile {id}: {profile_external_id}'.format(id=self.id, profile_external_id=self.profile_external_id)
