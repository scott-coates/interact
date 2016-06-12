from neo4jrestclient.client import Node

from src.domain.common import constants
from src.libs.graphdb_utils.services import graphdb_provider


def write_ea_to_graphdb(id, attrs, client_id, _graph_db_provider=graphdb_provider):
  gdb = _graph_db_provider.get_graph_client()

  q = '''
      MERGE (ea:EngagementAssignment {id: {engagement_assignment_id}})
      MATCH (client:Client {id: {client_id}})
      MERGE (client)-[:HAS_ASSIGNMENT]->(ea)
  '''

  params = {
    'engagement_assignment_id': id,
    'client_id': client_id,
  }

  if constants.EO_IDS in attrs:
    q += '''
        FOREACH (eo IN { eos } |
          MATCH (eo:EngagementOpportunity {id: eo.id})
          MERGE (eo)-[:ASSIGNED_TO]->(ea))
    '''

  q += '''
    RETURN ea
  '''

  params['eos'] = [{'id': eo_id} for eo_id in attrs[constants.EO_IDS]]

  ret_val = gdb.query(q, params=params, returns=(Node,))
  return ret_val[0][0]
