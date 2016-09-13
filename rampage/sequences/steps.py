
import logging
import os

from rampage.sequence import Step

LOG = logging.getLogger(__name__)

def image_create(clients, name):
    return Step(clients.glance.images.create,
                name=name,
                disk_format='qcow2',
                container_format='bare')

def image_upload(clients, create_step, image_file):
    def _image_upload():
        image_id = create_step.result['id']
        size = os.path.getsize(image_file)
        with open(image_file) as image_data:
            return clients.glance.images.upload(image_id, image_data,
                                                image_size=size)
    return Step(_image_upload)

def image_delete(clients, create_step):
    def _image_delete():
        image_id = create_step.result['id']
        # FIXME - delete image
    return Step(_image_delete)

def boot_server(clients, name, image_create_step, flavor_id):
    def _boot_server():
        image_id = image_create_step.result['id']
        return clients.nova.servers.create(name, image_id, flavor_id)
    return Step(_boot_server)

def wait_server(clients, boot_step):
    def _wait_server():
        server_id = boot_step.result.id
        # FIXME - wait for server to be ready
        return
    return Step(_wait_server)

def delete_server(clients, boot_step):
    def _delete_server():
        server_id = boot_step.result.id
        # FIXME - delete server
        return
    return Step(_delete_server)
