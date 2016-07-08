from src.apps.graph.client.repositories import write_client_to_graphdb, write_ta_topic_to_graphdb, \
  write_ea_to_graphdb, \
  retrieve_unassigned_grouped_entities_for_client_from_graphdb
from src.domain.common import constants


def create_client_in_graphdb(client_id):
  return write_client_to_graphdb(client_id).properties


def create_ta_topic_in_graphdb(client_id, ta_topic_id, relevance, topic_id):
  return write_ta_topic_to_graphdb(client_id, ta_topic_id, relevance, topic_id).properties


def create_ea_in_graphdb(id, attrs, client_id):
  return write_ea_to_graphdb(id, attrs, client_id).properties


def get_unassigned_grouped_entities_for_client_from_graphdb(client_id):
  ret_val = []

  query_val = retrieve_unassigned_grouped_entities_for_client_from_graphdb(client_id)

  for row in query_val:
    ret_val.append({constants.PROSPECT_ID: row[0], constants.EO_IDS: row[1]})

  return ret_val
