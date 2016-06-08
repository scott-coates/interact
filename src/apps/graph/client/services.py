from src.apps.graph.client.repositories import write_client_to_graphdb, write_ta_topic_to_graphdb


def create_client_in_graphdb(client_id):
  return write_client_to_graphdb(client_id).properties

def create_ta_topic_in_graphdb(client_id, ta_topic_id, topic_id):
  return write_ta_topic_to_graphdb(client_id, ta_topic_id, topic_id).properties
