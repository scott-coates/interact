from collections import namedtuple

ScoreAssignedEntityObject = namedtuple(
    'ScoreAssignedEntityObject',
    'assigned_entity_attrs assigned_entity_id assigned_entity_type provider_type prospect_id topic_ids'
)
