import logging
import unittest

from rampage import clients
from rampage.rampager import Rampager

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class TestRampage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRampage, self).__init__(*args, **kwargs)
        #self.clients = clients.Clients()
        self._rampage = Rampager()

    def setUp(self):
        LOG.info('running %s', __name__)

    def tearDown(self):
        LOG.info('running %s', __name__)
    def test_1(self):
        LOG.info('running %s', __name__)

    def test_kill_cpu(self):
        LOG.info('running %s', __name__)
        vm_ip = '10.4.154.230'
        self._rampage.time_cpu_usage(vm_ip,t_secs=30)

    @unittest.skip("Skipping test")
    def test_power_off_breakathon_vm(self):
        LOG.info('running %s', __name__)
        self._rampage.break_server_power('8329b1b8-67e7-4d5e-9e18-5a463a5da4aa')

    @unittest.skip("Skipping test")
    def test_power_on_breakathon_vm(self):
        LOG.info('running %s', __name__)
        self._rampage.restore_server_power('8329b1b8-67e7-4d5e-9e18-5a463a5da4aa')

