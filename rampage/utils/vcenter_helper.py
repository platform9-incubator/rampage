from pyVim import connect
from pyVmomi import vim
from pyVmomi import vmodl

import ssl
import os
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class VCHelper(object):

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
        self.envs = {}
        self.si = None
        self.load_vcenter_info_from_env()
        self.vmobj_cache = {}

    def __del__(self):
        """
        Clean stuff up
        :return:
        """
        if self.si is not None:
            connect.Disconnect(self.si)

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

        except vmodl.MethodFault as error:
            print "Caught vmodl fault : " + error.msg
            raise


    def get_vm_from_ip(self, ipaddr='10.4.123.150'):
        """
        Return VM context given an IP.
        :param ipaddr: IP Address as a string
        :return: VM Context if the VM with IP exists else None.
        """
        # Check if vm object already in cache. If yes, return the same object.
        if ipaddr in self.vmobj_cache and self.vmobj_cache[ipaddr] is not None:
            return self.vmobj_cache[ipaddr]
        res = None
        try:
            if self.si is None:
                self.get_si()

            #content = self.si.RetrieveContent()
            res = self.si.content.searchIndex.FindByIp(ip=ipaddr, vmSearch=True)
        except vmodl.RuntimeFault as error:
            print "Caught vmodl fault:" + error.msg
        self.vmobj_cache[ipaddr] = res
        return res

    def get_vm_from_name(self, name='arun-cirros-breakathon'):
        """
        Return VM context given the vm dns name.
        :param name: string name of vm
        :return: VM Context if the VM with name exists else None.
        """
        try:
            if self.si is None:
                self.get_si()

            #content = self.si.RetrieveContent()
            res = self.si.content.searchIndex.FindByDnsName(dnsName=name, vmSearch=True)
        except vmodl.RuntimeFault as error:
            print "Caught vmodl fault:" + error.msg
        return res

    def get_vm_from_uuid(self, uuid):
        """
        Return VM context given the vm uuid.
        :param name: string uuid of vm
        :return: VM Context if the VM with uuid exists else None.
        """
        try:
            if self.si is None:
                self.get_si()

            #content = self.si.RetrieveContent()
            res = self.si.content.searchIndex.FindByUuid(uuid=uuid, vmSearch=True,instanceUuid=True)
        except vmodl.RuntimeFault as error:
            print "Caught vmodl fault:" + error.msg
        return res

    def power_off_vm(self, vm_object):
        """
        Power off a given Virtual Machine
        :param vm_object: vm object for which we need to power off.
        :return:
        """
        LOG.debug("Powering off VM")
        vm_object.PowerOff()
        LOG.debug("Powered off VM")

    def power_on_vm(self, vm_object):
        """

        :param vm_object:
        :return:
        """
        LOG.debug("Powering on VM")
        vm_object.PowerOn()
        LOG.debug("Powered on VM")

    def hard_reboot_vm(self, vm_object):
        """

        :param vm_object:
        :return:
        """
        LOG.debug("Rebooting VM")
        res = vm_object.Reset()
        LOG.debug("Rebooted VM")
