from collections import defaultdict
from itertools import chain

from src.domain.common import constants
from src.domain.prospect.engagement_opportunity import service  as eo_service
from src.domain.prospect.events import ProspectCreated1, ProspectAddedProfile1, \
  EngagementOpportunityAddedToProfile1, TopicAddedToEngagementOpportunity1, ProspectUpdatedAttrsFromProfile1, \
  ProspectMarkedAsDuplicate, ProspectDeleted
from src.domain.prospect.profile import service as profile_service
from src.libs.common_domain.aggregate_base import AggregateBase
from src.libs.geo_utils.services import geo_location_service
from src.libs.web_utils.url.url_utils import get_unique_urls_from_iterable


class Prospect(AggregateBase):
  def __init__(self):
    super().__init__()
    self.is_duplicated = False
    self.is_deleted = False
    self.existing_prospect_id = None
    self._profiles = []

  @classmethod
  def from_attrs(cls, id, attrs):
    ret_val = cls()

    if not id:
      raise TypeError("id is required")

    if attrs is None:
      raise TypeError("attrs is required")

    ret_val._raise_event(ProspectCreated1(id, attrs))

    return ret_val

  def mark_as_duplicate(self, existing_prospect_id):
    if self.is_duplicated: raise Exception(self, 'already marked as duplicate.')
    self._raise_event(ProspectMarkedAsDuplicate(existing_prospect_id))
    if self.is_deleted: raise Exception(self, 'already marked as deleted.')
    self._raise_event(ProspectDeleted('Duplicate prospect. Existing prospect id: {0}.'.format(existing_prospect_id)))

  def consume_duplicate_prospect(self, duplicate_prospect):
    duplicate_prospect_profiles = duplicate_prospect._profiles

    for p in duplicate_prospect_profiles:
      existing_profile = self._find_profile_by_external_id_and_provider_type(p.external_id, p.provider_type)

      for eo in p._engagement_opportunities:
        existing_eo = self._find_eo_by_external_id_and_provider_type(eo.external_id, eo.provider_type)
        if not existing_eo:
          self._raise_event(EngagementOpportunityAddedToProfile1(eo.id, eo.external_id, eo.attrs, eo.provider_type,
                                                                 eo.provider_action_type, eo.created_date,
                                                                 self.is_duplicated,
                                                                 self.existing_prospect_id, existing_profile.id))

  def add_profile(self, id, external_id, provider_type, _profile_service=None, _geo_service=None):
    if not _profile_service: _profile_service = profile_service
    if not _geo_service: _geo_service = geo_location_service

    profile = self._find_profile_by_external_id_and_provider_type(external_id, provider_type)
    if profile: raise Exception(profile, 'already exists.')

    profile_attrs = _profile_service.get_profile_attrs_from_provider(external_id, provider_type)

    p_attrs = defaultdict(list)

    bio = profile_attrs.pop(constants.BIO, None)
    if bio:
      p_attrs[constants.BIOS].append(bio)

    location = profile_attrs.pop(constants.LOCATION, None)
    if location:
      location = _geo_service.get_geocoded_address_dict(location)
      p_attrs[constants.LOCATIONS].append(location)

    name = profile_attrs.pop(constants.NAME, None)
    if name:
      p_attrs[constants.NAMES].append(name)

    websites = profile_attrs.pop(constants.WEBSITES, None)
    if websites:
      combined_sites = self.attrs[constants.WEBSITES] + websites
      websites = get_unique_urls_from_iterable(combined_sites)
      p_attrs[constants.WEBSITES].extend(websites)

    self._raise_event(ProspectAddedProfile1(id, external_id, provider_type, profile_attrs))
    self._raise_event(ProspectUpdatedAttrsFromProfile1(p_attrs, id))

  def add_eo(self, id, external_id, attrs, provider_type,
             provider_action_type, created_date, profile_id, _eo_service=None):

    if not _eo_service: _eo_service = eo_service

    eo = self._find_eo_by_external_id_and_provider_type(external_id, provider_type)
    if eo: raise Exception(eo, 'already exists.')

    attrs = _eo_service.prepare_attrs_from_engagement_opportunity(attrs)

    self._raise_event(EngagementOpportunityAddedToProfile1(id, external_id,
                                                           attrs, provider_type,
                                                           provider_action_type, created_date, self.is_duplicated,
                                                           self.existing_prospect_id, profile_id))

  def add_topic_to_eo(self, eo_id, topic_id):
    self._raise_event(TopicAddedToEngagementOpportunity1(eo_id, topic_id))

  def _handle_created_1_event(self, event):
    self.id = event.id
    # noinspection PyArgumentList
    self.attrs = defaultdict(list, event.attrs)

  def _handle_profile_added_to_prospect_1_event(self, event):
    self._profiles.append(Profile(**event.data))

  def _handle_attrs_updated_from_profile_1_event(self, event):
    attrs = event.attrs
    self.attrs = attrs

  def _handle_eo_added_to_profile_1_event(self, event):
    profile = self._get_profile_by_id(event.profile_id)
    profile._add_eo(**event.data)

  def _handle_topic_added_to_eo_1_event(self, event):
    eo = self._get_eo_by_id(event.engagement_opportunity_id)
    eo._add_topic_id(event.topic_id)

  def _handle_marked_as_duplicate_1_event(self, event):
    self.is_duplicated = True
    self.existing_prospect_id = event.existing_prospect_id

  def _handle_deleted_1_event(self, event):
    self.is_deleted = True
    self.reason = event.reason

  def _get_profile_by_id(self, profile_id):
    profile = next(p for p in self._profiles if p.id == profile_id)

    return profile

  def _find_profile_by_external_id_and_provider_type(self, external_id, provider_type):
    profile = next(
        (p for p in self._profiles if p.external_id == external_id and p.provider_type == provider_type),
        None)

    return profile

  def _get_eo_by_id(self, eo_id):
    profiles = self._profiles
    eos = chain.from_iterable(p._engagement_opportunities for p in profiles)
    eo = next(eo for eo in eos if eo.id == eo_id)

    return eo

  def _find_eo_by_external_id_and_provider_type(self, external_id, provider_type):
    profiles = self._profiles

    eos = chain.from_iterable(p._engagement_opportunities for p in profiles)
    eo = next((eo for eo in eos if eo.external_id == external_id and eo.provider_type == provider_type), None)

    return eo

  def __str__(self):
    return 'Prospect {id}'.format(id=self.id)


class Profile:
  def __init__(self, id, external_id, provider_type, attrs, **kwargs):
    self._engagement_opportunities = []

    if not id:
      raise TypeError("id is required")

    if not external_id:
      raise TypeError("external_id is required")

    if not provider_type:
      raise TypeError("provider_type is required")

    if not attrs:
      raise TypeError("attrs is required")

    self.id = id
    self.external_id = external_id
    self.provider_type = provider_type
    self.attrs = attrs

  # noinspection PyUnusedLocal
  def _add_eo(self, id, external_id, attrs, provider_type, provider_action_type, created_date, **kwargs):
    eo = EngagementOpportunity(id, external_id, attrs, provider_type, provider_action_type, created_date)
    self._engagement_opportunities.append(eo)

  def _get_eo_by_id(self, eo_id):
    eo = next(eo for eo in self._engagement_opportunities if eo.id == eo_id)

    return eo

  def __str__(self):
    return 'Profile {id}: {external_id}'.format(id=self.id, external_id=self.external_id)


class EngagementOpportunity:
  def __init__(self, id, external_id, attrs, provider_type, provider_action_type, created_date):
    self._topic_ids = []

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

    if not created_date:
      raise TypeError("created_date is required")

    self.id = id
    self.external_id = external_id
    self.attrs = attrs
    self.provider_type = provider_type
    self.provider_action_type = provider_action_type
    self.created_date = created_date

  def _add_topic_id(self, topic_id):

    if not topic_id:
      raise TypeError("topic_id is required")

    if topic_id in self._topic_ids:
      raise Exception("{0} already has topic: {1}".format(self, topic_id))

    self._topic_ids.append(topic_id)

  def __str__(self):
    return 'EngagementOpportunity {id}: {external_id}'.format(id=self.id,
                                                              external_id=self.external_id)
