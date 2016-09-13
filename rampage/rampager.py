
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

    def break_server_power(self):
        pass

    def restore_server_power(self):
        pass

    def break_service(self):
        """
        Kill services such as ostackhost, hostagent, neutron, cider etc.
        :return:
        """
        pass

    def restore_service(self):
        pass

    def break_nfs_mount(self):
        pass

    def restore_nfs_mount(self):
        pass

    def break_data_network(self):
        pass

    def restore_data_network(self):
        pass

    def time_cpu_usage(self):
        pass

    def time_memory_usage(self):
        pass