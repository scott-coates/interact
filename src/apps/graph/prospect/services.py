from src.apps.graph.prospect.repositories import write_prospect_to_graphdb, write_profile_to_graphdb


def create_prospect_in_graphdb(profile_id):
  return write_prospect_to_graphdb(profile_id).properties


def create_profile_in_graphdb(prospect_id, profile_id):
  return write_profile_to_graphdb(prospect_id, profile_id).properties
