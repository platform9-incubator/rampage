from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl

import atexit
import ssl
import os

class VCHelper(object):
    envs = {}
    si = None

    def load_vcenter_info_from_env(self):
        """
        Load vcenter information
        :return:
        """
        self.envs['vsphere_user'] = os.getenv('VSPHERE_USERNAME', 'root')
        self.envs['vsphere_pass'] = os.getenv('VSPHERE_PASSWORD', 'ssssssss')
        self.envs['vsphere_url'] = os.getenv('VSPHERE_SERVER', 'vcva6-2.platform9.sys')
        self.envs['vsphere_port'] = os.getenv('VSPHERE_PORT', 443)

    def __init__(self):
        """
        Initialization
        """
        self.load_vcenter_info_from_env()


    def get_si(self):
        """
        Get Service Instance from VCenter
        :return:
        """
        try:
            default_context = ssl._create_default_https_context
            ssl._create_default_https_context = ssl._create_unverified_context
            self.si = connect.SmartConnect(host=self.envs['vsphere_url'],
                                                    user=self.envs['vsphere_user'],
                                                    pwd=self.envs['vsphere_pass'],
                                                    port=self.envs['vsphere_port'])
            ssl._create_default_https_context = default_context
            atexit.register(connect.Disconnect, self.si)

        except vmodl.MethodFault as error:
            print "Caught vmodl fault : " + error.msg
            raise


    def get_vm_from_ip(self, ipaddr='10.4.123.150'):
        """
        Return VM context given an IP.
        :param ipaddr: IP Address as a string
        :return: VM Context if the VM with IP exists else None.
        """
        res = None
        try:
            if self.si is None:
                self.get_si()

            content = self.si.RetrieveContent()
            res = content.searchIndex.FindByIp(ip=ipaddr, vmSearch=True)
        except vmodl.RuntimeFault as error:
            print "Caught vmodl fault:" + error.msg
        return res

    def power_off_vm(self, vm_object):
        """
        Power off a given Virtual Machine
        :param vm_object: vm object for which we need to power off.
        :return:
        """
