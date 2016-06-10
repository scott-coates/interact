from src.domain.prospect.engagement_opportunity import service  as eo_service
from src.domain.prospect.events import ProspectCreated1, Prospect1AddedProfile, \
  ProspectAddedEngagementOpportunityToProfile
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

  def add_profile(self, id, external_id, provider_type, _profile_service=None):
    if not _profile_service: _profile_service = profile_service
    if not id:
      raise TypeError("id is required")

    if not external_id:
      raise TypeError("external_id is required")

    if not provider_type:
      raise TypeError("provider_type is required")

    attrs = _profile_service.get_profile_attrs_from_provider(external_id, provider_type)

    self._raise_event(Prospect1AddedProfile(id, external_id, provider_type, attrs))

  def add_eo(self, id, external_id, attrs, provider_type,
             provider_action_type, created_at, profile_id, _eo_service=None):

    if not _eo_service: _eo_service = eo_service

    if not id:
      raise TypeError("id is required")

    if not external_id:
      raise TypeError("external_id is required")

    if not attrs:
      raise TypeError("attrs is required")

    if not provider_type:
      raise TypeError("provider_type is required")

    if not provider_action_type:
      raise TypeError("provider_action_type is required")

    if not created_at:
      raise TypeError("created_at is required")

    if not profile_id:
      raise TypeError("profile_id is required")

    attrs = _eo_service.prepare_attrs_from_engagement_opportunity(attrs)

    self._raise_event(ProspectAddedEngagementOpportunityToProfile(id, external_id,
                                                                  attrs, provider_type,
                                                                  provider_action_type, created_at, profile_id))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.attrs = event.attrs

  def _handle_profile_added_to_prospect_1_event(self, event):
    self._profiles.append(Profile(**event.data))

  def __str__(self):
    return 'Prospect {id}'.format(id=self.id)


class Profile:
  def __init__(self, id, external_id, provider_type, attrs):
    self._engagement_opportunities = []

    self.id = id
    self.external_id = external_id
    self.provider_type = provider_type
    self.attrs = attrs

  def __str__(self):
    return 'Profile {id}: {external_id}'.format(id=self.id, external_id=self.external_id)


class EngagementOpportunity:
  def __init__(self, id, external_id, provider_type, attrs):
    self._engagement_opportunities = []

    self.id = id
    self.external_id = external_id
    self.provider_type = provider_type
    self.attrs = attrs

  def __str__(self):
    return 'EngagementOpportunity {id}: {external_id}'.format(id=self.id,
                                                              external_id=self.external_id)
