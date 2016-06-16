from src.apps.relational.client.models import ProfileLookupForEA, ProspectLookupForEA
from src.apps.relational.prospect.models import ProfileLookupByProvider, EngagementOpportunityLookupByProvider


def save_profile_lookup_by_provider(profile_id, external_id, provider_type, prospect_id):
  profile, _ = ProfileLookupByProvider.objects.update_or_create(
      id=profile_id, defaults=dict(
          external_id=external_id, provider_type=provider_type, prospect_id=prospect_id
      )
  )

  return profile


def save_eo_lookup_by_provider(eo_id, external_id, provider_type, prospect_id):
  eo, _ = EngagementOpportunityLookupByProvider.objects.update_or_create(
      id=eo_id, defaults=dict(
          external_id=external_id, provider_type=provider_type, prospect_id=prospect_id
      )
  )

  return eo


def get_profile_lookup_from_provider_info(external_id, provider_type):
  return ProfileLookupByProvider.objects.get(external_id=external_id, provider_type=provider_type)


def get_profile_lookup(profile_id):
  return ProfileLookupByProvider.objects.get(id=profile_id)


def get_engagement_opportunity_lookup_from_provider_info(external_id, provider_type):
  return EngagementOpportunityLookupByProvider.objects.get(
      external_id=external_id, provider_type=provider_type)


def get_engagement_opportunity_lookup(eo_id):
  return EngagementOpportunityLookupByProvider.objects.get(id=eo_id)


def delete_prospect(prospect_id):
  ProfileLookupForEA.objects.filter(prospect_id=prospect_id).delete()
  ProspectLookupForEA.objects.filter(id=prospect_id).delete()
