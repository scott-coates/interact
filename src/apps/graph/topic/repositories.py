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
