import ovirtsdk4 as sdk
import ovirtsdk4.types as types

from utils import Connect
from utils import Output


class NetOps:
    def __init__(self):
        self.connect = Connect()
        self.c = self.connect.connect()

    def net_list(self, args):
        networks_service = self.c.system_service().networks_service()
        try:
            networks = networks_service.list()
            rows = []
            for network in networks:
                comment = ""
                description = ""
                if network.description is not None:
                    description = network.description
                if network.comment is not None:
                    comment = network.comment
                rows.append([network.id, network.name, comment, description])
            output = Output(["ID", "Name", "Comment", "Description"], rows)
            output.print_table()
            self.c.close()
        except sdk.Error as err:
            print "Failed to list networks, %s" % str(err)

    def net_add(self, args):
        vms_service = self.c.system_service().vms_service()
        vm = vms_service.list(search=args.vm_name)[0]
        nics_service = vms_service.vm_service(vm.id).nics_service()
        index = len(nics_service.list())
        # nics_service.add method takes vnic profile id as the variable,
        # not the network id. So we have to find out the vnic profile id
        # by using network id
        # https://lab-rhevm.gsslab.pek2.redhat.com/ovirt-engine/api/vnicprofiles/00e3cad9-5383-494c-9524-f353b5e2c8be
        profiles_service = self.c.system_service().vnic_profiles_service()
        profile_id = None
        for profile in profiles_service.list():
            if profile.network.id == args.net_id:
                profile_id = profile.id
                break
        nic_name = 'nic'+str(index)
        try:
            nics_service.add(
                types.Nic(
                    name=nic_name,
                    description='My network interface card',
                    vnic_profile=types.VnicProfile(
                        id=profile_id,
                    ),
                ),
            )
            self.c.close()
        except sdk.Error as err:
            print "Failed to add NICs to %s, %s" % (args.vm_name, str(err))

    def net_rm(self, args):
        vms_service = self.c.system_service().vms_service()
        vm = vms_service.list(search=args.vm_name)[0]
        nic_service = vms_service.vm_service(vm.id).nics_service().nic_service(args.port_id)

        #nics_service = vms_service.vm_service(vm.id).nics_service()
        #VmNicService got remove function
        # http://ovirt.github.io/ovirt-engine-sdk/master/services.m.html#ovirtsdk4.services.HostService.nics_service
        # nics_service.add method takes vnic profile id as the variable,
        # not the network id. So we have to find out the vnic profile id
        # by using network id
        # https://lab-rhevm.gsslab.pek2.redhat.com/ovirt-engine/api/vnicprofiles/00e3cad9-5383-494c-9524-f353b5e2c8be

        try:
            nic_service.remove(
                types.Nic(
                    name=nic_name,
                    description='My network interface card',
                    vnic_profile=types.VnicProfile(
                        id=profile_id,
                    ),
                ),
            )
            self.c.close()
        except sdk.Error as err:
            print "Failed to add NICs to %s, %s" % (args.vm_name, str(err))
