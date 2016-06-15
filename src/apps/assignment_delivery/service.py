from src.libs.analytics_utils.providers.keen import keen_client_service


def deliver_ea(ea_attrs):
  return keen_client_service.send_event('engagement_assigned', ea_attrs)
