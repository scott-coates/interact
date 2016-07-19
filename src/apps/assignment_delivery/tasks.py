import logging

from django_rq import job

from src.apps.assignment_delivery.service import deliver_ea_to_analytics_service, deliver_ea_to_read_model

logger = logging.getLogger(__name__)


@job('default')
def deliver_ea_to_analytics_service_task(ea_data):
  return deliver_ea_to_analytics_service(ea_data)


@job('default')
def deliver_ea_to_read_model_task(ea_data):
  return deliver_ea_to_read_model(ea_data)
