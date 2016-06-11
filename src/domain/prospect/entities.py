from itertools import chain

from src.domain.prospect.engagement_opportunity import service  as eo_service
from src.domain.prospect.events import ProspectCreated1, Prospect1AddedProfile, \
  EngagementOpportunityAddedToProfile1, TopicAddedToEngagementOpportunity1
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

    self._raise_event(EngagementOpportunityAddedToProfile1(id, external_id,
                                                           attrs, provider_type,
                                                           provider_action_type, created_at, profile_id))

  def add_topic_to_eo(self, eo_id, topic_id):

    if not eo_id:
      raise TypeError("eo_id is required")

    if not topic_id:
      raise TypeError("topic_id is required")

    eo = self._get_eo_by_id(eo_id)
    if topic_id in eo._topic_ids:
      raise Exception("eo: {0} already has topic: {1}".format(eo_id, topic_id))

    self._raise_event(TopicAddedToEngagementOpportunity1(eo_id, topic_id))

  def _handle_created_1_event(self, event):
    self.id = event.id
    self.attrs = event.attrs

  def _handle_profile_added_to_prospect_1_event(self, event):
    self._profiles.append(Profile(**event.data))

  def _handle_eo_added_to_profile_1_event(self, event):
    profile = self._get_profile_by_id(event.profile_id)
    profile._add_eo(**event.data)

  def _handle_topic_added_to_eo_1_event(self, event):
    profile = self._get_profile_by_id(event.profile_id)
    profile._add_topic_to_eo(event.engagement_opportunity_id, event.topic_id)

  def _get_profile_by_id(self, profile_id):
    profile = next(p for p in self._profiles if p.id == profile_id)

    return profile

  def _get_eo_by_id(self, eo_id):
    profiles = self._profiles
    eos = chain.from_iterable(p._engagement_opportunities for p in profiles)
    eo = next(eo for eo in eos if eo.id == eo_id)

    return eo

  def __str__(self):
    return 'Prospect {id}'.format(id=self.id)


class Profile:
  def __init__(self, id, external_id, provider_type, attrs):
    self._engagement_opportunities = []

    self.id = id
    self.external_id = external_id
    self.provider_type = provider_type
    self.attrs = attrs

  # noinspection PyUnusedLocal
  def _add_eo(self, id, external_id, provider_type, attrs, **kwargs):
    eo = EngagementOpportunity(id, external_id, provider_type, attrs)
    self._engagement_opportunities.append(eo)

  def _add_topic_to_eo(self, eo_id, topic_id):
    eo = self._get_eo_by_id(eo_id)
    eo._add_topic_id(topic_id)

  def _get_eo_by_id(self, eo_id):
    eo = next(eo for eo in self._engagement_opportunities if eo.id == eo_id)

    return eo

  def __str__(self):
    return 'Profile {id}: {external_id}'.format(id=self.id, external_id=self.external_id)


class EngagementOpportunity:
  def __init__(self, id, external_id, provider_type, attrs):
    self._topic_ids = []

    self.id = id
    self.external_id = external_id
    self.provider_type = provider_type
    self.attrs = attrs

  def _add_topic_id(self, topic_id):
    self._topic_ids.append(topic_id)

  def __str__(self):
    return 'EngagementOpportunity {id}: {external_id}'.format(id=self.id,
                                                              external_id=self.external_id)
