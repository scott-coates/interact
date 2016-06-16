import logging

from django_rq import job

from src.apps.assignment_delivery.service import deliver_ea

logger = logging.getLogger(__name__)


@job('default')
def deliver_ea_task(prospect_id, ea_data):
  return deliver_ea(prospect_id, ea_data)
