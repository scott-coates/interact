from src.apps.graph.topic.repositories import write_topic_to_graphdb


def create_topic_in_graphdb(topic_id):
  return write_topic_to_graphdb(topic_id).properties
