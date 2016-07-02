from unittest.mock import MagicMock

import pytest

from src.apps.relational.topic import service as topic_read_service
from src.domain.topic import service
from src.libs.python_utils.objects.object_utils import DynamicObject


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
])
def test_topic_service_finds_topics_in_tweet(content, ret_val):
  _topic_read_service = MagicMock(spec=topic_read_service)

  _topic_read_service.get_topic_lookups = MagicMock(
      return_value=[
        DynamicObject(id=1, name='real estate'),
        DynamicObject(id=2, name='software development'),
        DynamicObject(id=3, name='entrepreneurship'),
      ]
  )

  topic_ids = service.get_topic_ids_from_text(content, _topic_read_service=_topic_read_service)
  assert ret_val == topic_ids
