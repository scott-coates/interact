from unittest.mock import MagicMock

import pytest

from src.apps.read_model.relational.topic import service as topic_read_service
from src.apps.read_model.relational.topic.models import TopicLookup
from src.domain.topic import service
from src.domain.topic.service import get_topic_stems


@pytest.mark.parametrize(("content", "ret_val"), [
  ('@verlworkman @Shorewest Great Coaching Seminar!! Thanks so much! 2012 is already #Amazing!!! #realestate', [1]),
  ('Catch the latest on MKE Real Estate in the 7/15 @MKEBizJournal! Stu was part of a cool RE Roundtable today!', [1]),
  ("Learn More About ZyQuest's IT and Technology Services | http://buff.ly/28JgpWR | #software #developer #tech", [2]),
  ("""Get to know Foundry with "Continental Mapping Introduces http://TheGeoFoundry.com "
  http://www.slideshare.net/ContinentalMapping/continental-mapping-introduces-geofoundrycom … #softwaredevelopment""",
   [2]),
  ("5 Extraordinary #Business Lessons From Self-Made Billionaires http://bit.ly/28XHLbi #Entrepreneurship #Startup",
   [3]),
  ("Listening to interesting presentations about community entrepreneurship, closed loop supply chain, "
   "obsolscence,... ",
   [3]),
  ("RT @PostCrescent: .@FoxValleyTech is coming in with a 95 percent pass rate, making it a leader in the industry "
   "https://t.co/Q6SfYG4LwB",
   []),
  ("RT @Tamaraw68415067: Go Rubio! https://t.co/iZNMG19Svt",  # this one fails, it finds `ruby`
   []),
  ("Join me at the Women in Technology Annual Meeting! So many great things happening in #witwisconsin "
   "http://conta.cc/1tAAyVb  #constantcontact",
   [6]),
])
def test_topic_service_finds_topics_in_tweet(content, ret_val):
  _topic_read_service = MagicMock(spec=topic_read_service)

  _topic_read_service.get_topic_lookups = MagicMock(
      return_value=[
        _get_topic_mock(1, 'real estate'),
        _get_topic_mock(2, 'software development'),
        _get_topic_mock(3, 'entrepreneur'),
        _get_topic_mock(4, 'techie'),
        _get_topic_mock(5, 'ruby'),
        _get_topic_mock(6, 'women in tech'),
      ]
  )

  topic_ids = service.get_topic_ids_from_text(content, _topic_read_service=_topic_read_service)
  assert ret_val == topic_ids


def _get_topic_mock(id, name):
  stem, collapsed_stem = get_topic_stems(name)
  return MagicMock(spec=TopicLookup, id=id, name=name, stem=stem, collapsed_stem=collapsed_stem)
