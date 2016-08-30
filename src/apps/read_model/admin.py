import json

from django.contrib import admin
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import JsonLexer

from src.apps.read_model.relational.client.models import DeliveredEa
from src.domain.common import constants


class DeliveredEaAdmin(admin.ModelAdmin):
  readonly_fields = ('score_attrs_pretty',)

  actions = None
  list_display = ('name', 'location', 'bio', 'score', 'batch_id')

  def has_delete_permission(self, request, obj=None):
    return False

  def has_add_permission(self, request):
    return False

  # Allow viewing objects but not actually changing them
  # https://gist.github.com/aaugustin/1388243
  def has_change_permission(self, request, obj=None):
    if request.method not in ('GET', 'HEAD'):
      return False
    return super().has_change_permission(request, obj)

  # def get_readonly_fields(self, request, obj=None):
  #   return (self.fields or [f.name for f in self.model._meta.fields]) + list(DeliveredEaAdmin.readonly_fields)

  def score_attrs_pretty(self, instance):
    """Function to display pretty version of our data"""
    # Convert the data to sorted, indented JSON
    response = json.dumps(instance.score_attrs[constants.SCORE][constants.SCORE_ATTRS], sort_keys=True, indent=2)

    # Get the Pygments formatter
    formatter = HtmlFormatter(style='colorful')

    # Highlight the data
    response = highlight(response, JsonLexer(), formatter)

    # Get the stylesheet
    style = "<style>" + formatter.get_style_defs() + "</style><br>"

    # Safe the output
    return mark_safe(style + response)

  score_attrs_pretty.short_description = 'Score Attrs'


admin.site.register(DeliveredEa, DeliveredEaAdmin)
