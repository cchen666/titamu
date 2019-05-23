import ovirtsdk4 as sdk
import ovirtsdk4.types as types

from utils import Connect
from utils import Output


class DiskOps:
    def __init__(self):
        self.connect = Connect()
        self.c = self.connect.connect()

    def disk_add(self, args):
        vms_service = self.c.system_service().vms_service()
        vm = vms_service.list(search=args.vm_name)[0]
        disk_attachments_service = vms_service.vm_service(vm.id).disk_attachments_service()

        disk_attachments_service.add(
            types.DiskAttachment(
                disk=types.Disk(
                    name='mydisk',
                    description='Created by titamu',
                    format=types.DiskFormat.COW,
                    provisioned_size=args.size * 2 ** 30,
                    storage_domains=[
                        types.StorageDomain(
                            name=storagedomain,
                        ),
                    ],
                ),
                interface=types.DiskInterface.VIRTIO,
                bootable=False,
                active=True,
            ),
        )

    def disk_list(self, args):
        try:
            vms_service = self.c.system_service().vms_service()
            vm = vms_service.list(search=args.vm_name)[0]
            vm_service = vms_service.vm_service(vm.id)
            disk_attachments_service = vm_service.disk_attachments_service()
            disk_attachments = disk_attachments_service.list()
            rows=[]
            for disk_attachment in disk_attachments:
                disk = self.c.follow_link(disk_attachment.disk)
                rows.append([disk.id, disk.name, str(disk.provisioned_size / 1024 / 1024 / 1024) + "G", str(disk.status).upper()])

            output = Output(["ID", "Name","Size" , "Status"], rows)
            output.print_table()
            self.c.close()
        except sdk.Error as err:
            print "Failed to list disks, %s" % str(err)
