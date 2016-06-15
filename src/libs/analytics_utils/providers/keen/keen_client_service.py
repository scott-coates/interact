from src.libs.analytics_utils.providers.keen.keen_client_provider import get_keen_client


def send_event(name, properties):
  client = get_keen_client()

  ret_val = client.add_event(name, properties)

  return ret_val
