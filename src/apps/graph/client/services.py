from src.apps.graph.client.repositories import write_client_to_graphdb


def create_client_in_graphdb(client_id):
  return write_client_to_graphdb(client_id).properties
