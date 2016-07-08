from neo4jrestclient.client import Node, Relationship

from src.domain.common import constants
from src.libs.graphdb_utils.services import graphdb_provider


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


def write_ta_topic_to_graphdb(client_id, ta_topic_id, relevance, topic_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
    MATCH (client_id:Client), (topic:Topic)
    WHERE client_id.id = { client_id }
    AND topic.id = { topic_id }
    MERGE (client_id)-[r:TA_TOPIC {id: {ta_topic_id}, relevance: {relevance}}]->(topic)
    RETURN r
  '''

  params = {
    'client_id': client_id,
    'ta_topic_id': ta_topic_id,
    'relevance': relevance,
    'topic_id': topic_id,
  }

  ret_val = gdb.query(q, params=params, returns=(Relationship,))

  return ret_val[0][0]


def write_ea_to_graphdb(id, attrs, client_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MERGE (ea:EngagementAssignment {id: {engagement_assignment_id}})
      WITH ea
      MATCH (client_id:Client {id: {client_id}})
      MERGE (client_id)-[:HAS_ASSIGNMENT]->(ea)
  '''

  params = {
    'engagement_assignment_id': id,
    'client_id': client_id,
  }

  if constants.EO_IDS in attrs:
    params['eo_ids'] = attrs[constants.EO_IDS]

    q += '''
    WITH ea
    MATCH (eo:EngagementOpportunity)
    WHERE eo.id IN {eo_ids}
    MERGE (eo)-[:ASSIGNED_TO]->(ea)
    '''

  q += '''
    RETURN ea
  '''

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]


def retrieve_unassigned_grouped_entities_for_client_from_graphdb(client_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      // start by limit the client_id and its topics
      MATCH (client_id:Client {id: {client_id}})-[rel_client_has_topic:TA_TOPIC]->(topic:Topic),

      // start query for getting potential eos
      (eo:EngagementOpportunity)-[rel_eo_topic:ENGAGEMENT_OPPORTUNITY_TOPIC]->(topic),
      (eo)-[rel_eo_belongs_to_profile:BELONGS_TO]-(profile:Profile),
      (profile)-[rel_profile_belongs_to_prospect:BELONGS_TO]->(prospect:Prospect)

      // do the filtering
      WHERE NOT (eo)-[:ASSIGNED_TO]->(:EngagementAssignment)

      // make sure to call distinct because when a prospect has multiple profiles, a row will be returned for each
      // profile
      WITH
        collect(distinct(eo.id)) as eos,
        prospect.id as prospect

      RETURN prospect, eos
  '''

  params = {
    'client_id': client_id,
  }

  query_val = gdb.query(q, params=params, returns=(str, list))

  return query_val
