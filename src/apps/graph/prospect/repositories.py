from neo4jrestclient.client import Node

from src.libs.graphdb_utils.services import graphdb_provider


def write_prospect_to_graphdb(prospect_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MERGE (n:Prospect {id: {prospect_id}})
      RETURN n
  '''

  params = {
    'prospect_id': prospect_id,
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]


def delete_prospect_from_graphdb(prospect_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MATCH (prospect:Prospect {id: {prospect_id}})
      OPTIONAL MATCH (prospect)<-[:BELONGS_TO]-(profile:Profile)
      OPTIONAL MATCH (profile)<-[:BELONGS_TO]-(eo:EngagementOpportunity)
      DETACH DELETE prospect, profile, eo
  '''

  params = {
    'prospect_id': prospect_id,
  }

  ret_val = gdb.query(q, params=params)

  return ret_val


def write_profile_to_graphdb(prospect_id, profile_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (prospect:Prospect {id: { prospect_id }})
    MERGE (profile:Profile {id: {profile_id}})
    MERGE (profile)-[:BELONGS_TO]->(prospect)
    RETURN profile
  '''
  params = {
    'prospect_id': prospect_id,
    'profile_id': profile_id,
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))

  return ret_val[0][0]


def write_eo_to_graphdb(profile_id, eo_id, topic_ids, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (profile:Profile {id:{profile_id}})
    MATCH (topic:Topic)
    WHERE topic.id IN {topic_ids}
    MERGE (eo:EngagementOpportunity {id: {eo_id}})
    MERGE (eo)-[:BELONGS_TO]->(profile)
    MERGE (eo)-[r:ENGAGEMENT_OPPORTUNITY_TOPIC]->(topic)
    RETURN eo
  '''
  params = {
    'profile_id': profile_id,
    'eo_id': eo_id,
    'topic_ids': topic_ids,
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))

  return ret_val[0][0]
