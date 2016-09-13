import logging
import unittest

from rampage.utils.vcenter_helper import VCHelper
from rampage import clients

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

class TestRampage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRampage, self).__init__(*args, **kwargs)
        self.clients = clients.Clients()

    def setUp(self):
        LOG.info('running %s', __name__)
    def tearDown(self):
        LOG.info('running %s', __name__)
    def test_1(self):
        LOG.info('running %s', __name__)

    def test_2(self):
        obj = VCHelper()
        vm_obj = obj.get_vm_from_ip()
        print vm_obj
