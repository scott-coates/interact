from src.libs.analytics_utils.providers.keen import keen_client_service
from src.apps.relational.client.service import get_prospect_ea_lookup, get_profile_ea_lookups_by_prospect_id
from src.domain.common import constants


def deliver_ea(prospect_id, ea_data):
  event_data = {}

  prospect = get_prospect_ea_lookup(prospect_id)
  profiles = get_profile_ea_lookups_by_prospect_id(prospect)
  event_data[constants.PROSPECT] = prospect.attrs
  event_data[constants.PROFILES] = [p.profile_attrs for p in profiles]

  event_data[constants.ENGAGEMENT_ASSIGNMENT] = ea_data

  return keen_client_service.send_event('engagement_assigned', event_data)
