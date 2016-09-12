import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

class TestRampage(unittest.TestCase):
    def setUp(self):
        LOG.info('running %s', __name__)
    def tearDown(self):
        LOG.info('running %s', __name__)
    def test_1(self):
        LOG.info('running %s', __name__)
