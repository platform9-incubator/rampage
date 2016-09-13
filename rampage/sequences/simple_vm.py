import logging

from rampage.sequence import Sequence
from rampage.clients import Clients
from rampage.sequences import steps

LOG = logging.getLogger(__name__)

class SimpleVmSequence(Sequence):
    def __init__(self, max_step_failures):
        super(SimpleVmSequence, self).__init__(max_step_failures)
        self.clients = Clients()
        image_file = '/home/rdeuel/images/cirros-0.3.4-x86_64-disk.img'
        image_create = steps.image_create(self.clients, 'cirros')
        image_upload = steps.image_upload(self.clients, image_create,
                                          image_file)
        server_boot = steps.boot_server(self.clients, 'simple-vm',
                                        image_create, 1)
        server_wait = steps.wait_server(self.clients, server_boot)
        server_delete = steps.delete_server(self.clients, server_boot)
        image_delete = steps.image_delete(self.clients, image_create)

        for step in [image_create, image_upload, server_boot,
                     server_wait, server_delete, image_delete]:
            self.add_step(step)

