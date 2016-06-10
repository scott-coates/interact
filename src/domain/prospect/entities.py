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

  def add_eo(self, id, engagement_opportunity_external_id, engagement_opportunity_attrs, provider_type,
             provider_action_type, created_at, profile_id, _eo_service=None):

    if not _eo_service: _eo_service = profile_service

    if not id:
      raise TypeError("id is required")

    if not engagement_opportunity_external_id:
      raise TypeError("engagement_opportunity_external_id is required")

    if not engagement_opportunity_attrs:
      raise TypeError("engagement_opportunity_attrs is required")

    if not provider_type:
      raise TypeError("provider_type is required")

    if not provider_action_type:
      raise TypeError("provider_action_type is required")

    if not created_at:
      raise TypeError("created_at is required")
    
    if not profile_id:
      raise TypeError("profile_id is required")

    attrs = _eo_service.get_profile_attrs_from_provider(profile_external_id, provider_type)

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
    self._engagement_opportunities = []

    self.id = id
    self.profile_external_id = profile_external_id
    self.provider_type = provider_type
    self.attrs = attrs

  def __str__(self):
    return 'Profile {id}: {profile_external_id}'.format(id=self.id, profile_external_id=self.profile_external_id)


class EngagementOpportunity:
  def __init__(self, id, engagement_opportunity_external_id, provider_type, attrs):
    self._engagement_opportunities = []

    self.id = id
    self.profile_external_id = profile_external_id
    self.provider_type = provider_type
    self.attrs = attrs

  def __str__(self):
    return 'EngagementOpportunity {id}: {profile_external_id}'.format(id=self.id,
                                                                      profile_external_id=self.profile_external_id)
