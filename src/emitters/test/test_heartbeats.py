import unittest

from ..heartbeats import *


class TestStaleInfraQueryBuilder(unittest.TestCase):

    def test_create_es_query_temporal(self):
        q = create_es_query(minutes=120, size=100)
        # Changing the time range can cause the query to not retrieve cotravelers as designed
        self.assertEqual(q['query']['bool']['must'][0]['range']['heartbeat']['lte'], "now-120m")

    def test_create_es_query_size(self):
        q = create_es_query(minutes=120, size=100)
        # Increased size can hurt performance, decreased size can cause the storyline to break up.
        self.assertEqual(q['size'], 100)


if __name__ == '__main__':
    unittest.main()
