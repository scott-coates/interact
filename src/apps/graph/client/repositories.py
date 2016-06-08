from src.libs.graphdb_utils.services import graphdb_provider
from neo4jrestclient.client import Node, Relationship


def write_client_to_graphdb(client_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MERGE (n:Client {id: {client_id}})
      RETURN n
  '''

  params = {
    'client_id': client_id,
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]


#
# def delete_client_from_graphdb(client_id, _graph_db_provider=graphdb_provider):
#   gdb = _graph_db_provider.get_graph_client()
#
#   q = """
#     MATCH (client:Client)
#     WHERE client.client_id = { client_id }
#     OPTIONAL MATCH (client)-[ta:TA_TOPIC]-()
#     OPTIONAL MATCH (client)<-[assigned:ASSIGNED_TO]-(ea:EngagementAssignment)
#     DELETE ta, assigned, ea, client
#   """
#   client_id = client_id
#
#   params = {
#     'client_id': client_id,
#   }
#
#   ret_val = gdb.query(q, params=params)
#
#   return ret_val


def write_ta_topic_to_graphdb(client_id, ta_topic_id, topic_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (client:Client), (topic:Topic)
    WHERE client.id = { client_id }
    AND topic.id = { topic_id }
    MERGE (client)-[r:TA_TOPIC]->(topic)
    SET r.id = { ta_topic_id }
    RETURN r
  '''

  ta_topic_id = ta_topic_id
  topic_id = topic_id
  params = {

    'client_id': client_id,
    'ta_topic_id': ta_topic_id,
    'topic_id': topic_id,

  }

  ret_val = gdb.query(q, params=params, returns=(Relationship,))

  return ret_val[0][0]

#
# def delete_ta_topic_from_graphdb(client_id, ta_topic_id, _graph_db_provider=graphdb_provider):
#   gdb = _graph_db_provider.get_graph_client()
#
#   q = '''
#     MATCH (client:Client)
#     WHERE client.client_id = { client_id }
#     MATCH (client)-[r:TA_TOPIC]->(topic:Topic)
#     WHERE r.ta_topic_id = { ta_topic_id }
#     DELETE r
#   '''
#
#   ta_topic_id = ta_topic_id
#
#   params = {
#
#     'client_id': client_id,
#     'ta_topic_id': ta_topic_id,
#   }
#
#   ret_val = gdb.query(q, params=params, returns=(Relationship,))
#
#   return ret_val
