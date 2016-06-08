from src.apps.graph.topic.repositories import write_topic_to_graphdb


def create_topic_in_graphdb(topic_id):
  return write_topic_to_graphdb(topic_id).properties

#
# def create_subtopic_in_graphdb(topic_id, subtopic_id):
#   return write_subtopic_to_graphdb(topic_id, subtopic_id).properties
#
#
# def delete_topic_in_graphdb(topic_id):
#   delete_topic_from_graphdb(topic_id)
#   return topic_id
#
#
# def delete_subtopic_in_graphdb(topic_id, subtopic_id):
#   delete_subtopic_from_graphdb(topic_id, subtopic_id)
#   return subtopic_id
