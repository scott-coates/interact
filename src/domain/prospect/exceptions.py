class DuplicateProspectError(Exception):
  """A duplicate prospect was detected"""

  def __init__(self, existing_prospect_id, duplicate_prospect_id, *args, **kwargs):
    self.existing_prospect_id = existing_prospect_id
    self.duplicate_prospect_id = duplicate_prospect_id
    super().__init__(*args, **kwargs)

  def __str__(self):
    return repr((self.existing_prospect_id, self.duplicate_prospect_id))
