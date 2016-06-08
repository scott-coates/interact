from src.libs.graphdb_utils.services import graphdb_provider
from neo4jrestclient.client import Node


def write_topic_to_graphdb(topic_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MERGE (n:Topic {id: {topic_id}})
      RETURN n
  '''

  params = {
    'topic_id': topic_id,
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]
#
#
# def delete_topic_from_graphdb(topic_id, _graph_db_provider=graphdb_provider):
#   gdb = _graph_db_provider.get_graph_client()
#
#   q = """
#       MATCH (topic:Topic)
#       WHERE topic.topic_id = { topic_id }
#       MATCH (topic)-[r]-()
#       OPTIONAL MATCH (topic)<-[eor:ENGAGEMENT_OPPORTUNITY_TOPIC]-(eo:EngagementOpportunity)
#       OPTIONAL MATCH (topic)<-[str:BELONGS_TO]-(st:Subtopic)
#       DELETE r, eor, eo, str, st, topic
#     """
#   topic_id = topic_id
#
#   params = {
#     'topic_id': topic_id,
#   }
#
#   ret_val = gdb.query(q, params=params)
#
#   return ret_val
#
#
# def delete_subtopic_from_graphdb(topic_id, subtopic_id, _graph_db_provider=graphdb_provider):
#   gdb = _graph_db_provider.get_graph_client()
#
#   q = """
#       MATCH (subtopic:Subtopic)
#       WHERE subtopic.subtopic_id = { subtopic_id }
#       MATCH (topic:Topic)
#       WHERE topic.topic_id = { topic_id }
#       MATCH (subtopic)-[r:BELONGS_TO]->(topic)
#       DELETE r, subtopic
#     """
#   topic_id = topic_id
#
#   params = {
#     'topic_id': topic_id,
#     'subtopic_id': subtopic_id,
#   }
#
#   ret_val = gdb.query(q, params=params)
#
#   return ret_val
#
#
# def write_subtopic_to_graphdb(topic_id, subtopic_id, _graph_db_provider=graphdb_provider):
#   gdb = _graph_db_provider.get_graph_client()
#
#   q = '''
#       MATCH (topic:Topic)
#       WHERE topic.topic_id = { topic_id }
#       CREATE (subtopic:Subtopic)-[:BELONGS_TO]->(topic)
#       SET subtopic.subtopic_id = { subtopic_id }
#       RETURN topic
#   '''
#
#   params = {
#
#     "topic_id": topic_id,
#     "subtopic_id": subtopic_id,
#
#   }
#
#   ret_val = gdb.query(q, params=params, returns=(Node,))
#   return ret_val[0][0]
