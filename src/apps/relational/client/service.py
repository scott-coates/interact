import logging

from src.apps.relational.client.models import ActiveTATopicOption, ProspectLookupForEA, ProfileLookupForEA, \
  EOLookupForEA, ClientLookupForEA, TopicLookupForClient
from src.domain.common import constants

logger = logging.getLogger(__name__)


def save_topic_lookup(id, stem):
  topic, _ = TopicLookupForClient.objects.update_or_create(
      id=id, defaults=dict(
          snowball_stem=stem
      )
  )

  return topic


def get_active_ta_topic_options():
  active_topics = ActiveTATopicOption.objects.all()
  return active_topics


def get_ta_topic_option(ta_topic_option_id):
  return ActiveTATopicOption.objects.get(id=ta_topic_option_id)


def save_active_ta_topic_option(id, option_name, option_type, option_attrs, ta_topic_id, topic_id, client_id):
  at, _ = ActiveTATopicOption.objects.update_or_create(
      id=id, defaults=dict(
          option_name=option_name, option_type=option_type,
          option_attrs=option_attrs, ta_topic_id=ta_topic_id,
          topic_id=topic_id, client_id=client_id
      )
  )
  return at


def save_client_ea_lookup(id, ta_attrs):
  client, _ = ClientLookupForEA.objects.update_or_create(
      id=id, defaults=dict(
          ta_attrs=ta_attrs
      )
  )
  return client


def save_topic_to_client_ea_lookup(client_id, topic_id):
  client = get_client_ea_lookup(client_id)
  topic = get_client_topic_lookup(topic_id)
  client.ta_topics[topic_id] = {constants.SNOWBALL_STEM: topic.snowball_stem}
  client.save()
  return client


def save_prospect_ea_lookup(id, attrs):
  prospect, _ = ProspectLookupForEA.objects.update_or_create(
      id=id, defaults=dict(
          attrs=attrs
      )
  )
  return prospect


def save_profile_ea_lookup(id, profile_attrs, provider_type, prospect_id):
  profile, _ = ProfileLookupForEA.objects.update_or_create(
      id=id, defaults=dict(
          provider_type=provider_type, profile_attrs=profile_attrs, prospect_id=prospect_id
      )
  )
  return profile


def save_eo_ea_lookup(id, eo_attrs, provider_type, profile_id, prospect_id):
  eo, _ = EOLookupForEA.objects.update_or_create(
      id=id, defaults=dict(
          eo_attrs=eo_attrs, provider_type=provider_type, profile_id=profile_id, prospect_id=prospect_id
      )
  )
  return eo


def save_topic_to_eo_ea_lookup(eo_id, topic_id):
  eo = EOLookupForEA.objects.get(id=eo_id)
  eo.topic_ids[topic_id] = True
  eo.save()
  return eo


def get_client_topic_lookup(id):
  return TopicLookupForClient.objects.get(id=id)


def get_client_ea_lookup(id):
  return ClientLookupForEA.objects.get(id=id)


def get_prospect_ea_lookup(id):
  return ProspectLookupForEA.objects.get(id=id)


def get_profile_ea_lookups_by_prospect_id(prospect_id):
  return ProfileLookupForEA.objects.filter(prospect_id=prospect_id)


def get_eo_ea_lookup(id):
  return EOLookupForEA.objects.get(id=id)
