from src.apps.graph.prospect.repositories import write_prospect_to_graphdb, write_profile_to_graphdb, \
  write_eo_to_graphdb, delete_prospect_from_graphdb


def create_prospect_in_graphdb(profile_id):
  return write_prospect_to_graphdb(profile_id).properties


def delete_prospect_in_graphdb(prospect_id):
  delete_prospect_from_graphdb(prospect_id)
  return prospect_id


def create_profile_in_graphdb(prospect_id, profile_id):
  return write_profile_to_graphdb(prospect_id, profile_id).properties


def create_eo_in_graphdb(profile_id, eo_id, topic_ids):
  return write_eo_to_graphdb(profile_id, eo_id, topic_ids).properties
