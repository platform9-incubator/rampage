from rampage.utils.vcenter_helper import VCHelper
from paramiko import SSHClient
from scp import SCPClient

import logging
import os
import paramiko
import time


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Rampager(object):
    """
    Define methods here that will cause rampage.
    Each "break_" method should have a corresponding "restore_" method
    that will heal the breakage.
    If your break functionality self heals (say timing based), use the
    keyword "time_" to start your method.
    @todo Add "other" support here.
    @todo Add providers instead of directly using vcenter provider.
    """
    def __init__(self):
        self.vc = VCHelper()
        self._ssh = SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __del__(self):
        if self._ssh._transport:
            self._ssh.close()

    def _connect_to_host(self, host_ip):
        # Check if already connected
        if self._ssh._transport:
            return
        self._ssh.connect(host_ip, os.getenv('HOST_PORT', 22),
                          os.getenv('HOST_USERNAME', 'ubuntu'),
                          os.getenv('HOST_PASSWORD', 'ubuntu'))

    def break_server_power(self, server_uuid):
        LOG.debug("Executing break power task for server uuid: %s" % server_uuid)
        vm_obj = self.vc.get_vm_from_uuid(server_uuid)
        if vm_obj:
            self.vc.power_off_vm(vm_obj)

    def restore_server_power(self, server_uuid):
        LOG.debug("Executing restore power task for server uuid: %s" % server_uuid)
        vm_obj = self.vc.get_vm_from_uuid(server_uuid)
        if vm_obj:
            self.vc.power_on_vm(vm_obj)

    def break_service(self, server_ip):
        """
        Kill services such as ostackhost, hostagent, neutron, cider etc.
        :return:
        """
        pass

    def restore_service(self, server_ip):
        pass

    def break_nfs_mount(self, server_ip):
        pass

    def restore_nfs_mount(self, server_ip):
        pass

    def break_data_network(self, server_ip):
        pass

    def restore_data_network(self, server_ip):
        pass

    def time_cpu_usage(self, server_ip, t_secs=20, threads=None):
        LOG.debug("Executing increased cpu load on %s for %s seconds" % (server_ip, time))
        self._connect_to_host(server_ip)
        with SCPClient(self._ssh.get_transport()) as scp:
            scp.put('rampage/utils/kill_cpu.sh', remote_path="/tmp/" )
        cmd = '/tmp/kill_cpu.sh %s' % t_secs
        if threads:
            cmd += " %s" % threads
        self._ssh.exec_command(cmd)
        time.sleep(t_secs)


    def time_memory_usage(self, server_ip):
        pass