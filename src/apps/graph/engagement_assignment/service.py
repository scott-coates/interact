from src.apps.graph.engagement_assignment.repositories import write_ea_to_graphdb


def create_ea_in_graphdb(id, attrs, client_id):
  return write_ea_to_graphdb(id, attrs, client_id).properties
