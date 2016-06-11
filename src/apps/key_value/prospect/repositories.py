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


def write_profile_to_graphdb(prospect_id, profile_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (prospect:Prospect)
    WHERE prospect.id = { prospect_id }
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


def write_eo_to_graphdb(profile_id, eo_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (profile:Profile)
    WHERE profile.id = { profile_id }
    MERGE (eo:EngagementOpportunity {id: {eo_id}})
    MERGE (eo)-[:BELONGS_TO]->(profile)
    RETURN eo
  '''
  params = {
    'profile_id': profile_id,
    'eo_id': eo_id,
  }

  ret_val = gdb.query(q, params=params, returns=(Node,))

  return ret_val[0][0]