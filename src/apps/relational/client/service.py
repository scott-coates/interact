import logging

from django.db import transaction

from src.apps.relational.client.models import ActiveTaTopicOption, ProspectLookupForEa, ProfileLookupForEa, \
  EoLookupForEa, ClientLookupForEa, EaToDeliver
from src.apps.relational.topic.service import get_topic_lookup
from src.domain.common import constants

logger = logging.getLogger(__name__)


def get_active_ta_topic_options():
  active_topics = ActiveTaTopicOption.objects.all()
  return active_topics


def get_ta_topic_option(ta_topic_option_id):
  return ActiveTaTopicOption.objects.get(id=ta_topic_option_id)


def save_active_ta_topic_option(id, option_name, option_type, option_attrs, ta_topic_id, ta_topic_relevance,
                                topic_id, client_id):
  at, _ = ActiveTaTopicOption.objects.update_or_create(
      id=id, defaults=dict(
          option_name=option_name, option_type=option_type,
          option_attrs=option_attrs, ta_topic_id=ta_topic_id, ta_topic_relevance=ta_topic_relevance,
          topic_id=topic_id, client_id=client_id
      )
  )
  return at


def save_client_ea_lookup(id, ta_attrs):
  client, _ = ClientLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          ta_attrs=ta_attrs
      )
  )
  return client


def save_topic_to_client_ea_lookup(client_id, relevance, topic_id):
  with transaction.atomic():
    client = get_client_ea_lookup(client_id)
    topic = get_topic_lookup(topic_id)
    client.ta_topics[topic_id] = {
      constants.NAME: topic.name,
      constants.RELEVANCE: relevance
    }

    client.save()

  return client


def save_prospect_ea_lookup(id, attrs):
  prospect, _ = ProspectLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          attrs=attrs
      )
  )
  return prospect


def save_topics_to_prospect_ea_lookup(prospect_id, topic_ids):
  with transaction.atomic():
    prospect = get_prospect_ea_lookup(prospect_id)
    prospect.topic_ids.extend(topic_ids)
    prospect.save()

  return prospect


def save_profile_ea_lookup(id, profile_attrs, provider_type, prospect_id):
  profile, _ = ProfileLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          provider_type=provider_type, profile_attrs=profile_attrs, prospect_id=prospect_id
      )
  )
  return profile


def save_eo_ea_lookup(id, eo_attrs, topic_ids, provider_type, profile_id, prospect_id):
  eo, _ = EoLookupForEa.objects.update_or_create(
      id=id, defaults=dict(
          eo_attrs=eo_attrs, topic_ids=topic_ids,
          provider_type=provider_type, profile_id=profile_id,
          prospect_id=prospect_id
      )
  )
  return eo


def get_client_ea_lookup(id):
  return ClientLookupForEa.objects.get(id=id)


def get_prospect_ea_lookup(id):
  return ProspectLookupForEa.objects.get(id=id)


def get_profile_ea_lookups_by_prospect_id(prospect_id):
  return ProfileLookupForEa.objects.filter(prospect_id=prospect_id)


def get_eo_ea_lookup(id):
  return EoLookupForEa.objects.get(id=id)


def delete_prospect(prospect_id):
  ProfileLookupForEa.objects.filter(prospect_id=prospect_id).delete()
  EoLookupForEa.objects.filter(prospect_id=prospect_id).delete()
  ProspectLookupForEa.objects.filter(id=prospect_id).delete()


def save_ea_deliver(ea_id, score, score_attrs, client_id, prospect_id):
  eo, _ = EaToDeliver.objects.update_or_create(
      id=ea_id, defaults=dict(
          score=score, score_attrs=score_attrs,
          client_id=client_id, prospect_id=prospect_id,
      )
  )
  return eo


def get_ea_deliver(id):
  return EaToDeliver.objects.get(id=id)

def delete_ea_deliver(id):
  return get_ea_deliver(id).delete()
