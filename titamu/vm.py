import ovirtsdk4 as sdk
import ovirtsdk4.types as types
import subprocess

from os import environ
from utils import Connect
from utils import Output


class VmOps:
    def __init__(self):
        self.connect = Connect()
        self.c = self.connect.connect()

    def test(self):
        print self.c

    def vm_list(self, args):
        # Call ovirtsdk to get vms_service
        vms_service = self.c.system_service().vms_service()
        # We check whether prefix has been given or not
        if args.prefix is not None:
            search_prefix = 'name=' + args.prefix + '*'
        else:
            search_prefix = 'name=' + environ.get('TITAMU_VM_PREFIX') + '*'
        try:
            # Get vm list by using vms_service
            vms = vms_service.list(
                search=search_prefix,
                case_sensitive=False,
            )
            rows = []
            for vm in vms:
                addr = ""
                comment = ""
                if vm.comment is not None:
                    comment = vm.comment
                vm_service = vms_service.vm_service(vm.id)
                # We use reported_devices_service method to get all the
                # NICs that have IP address assigned
                for device in vm_service.reported_devices_service().list():
                    if device.ips is not None and vm.status.value == 'up':
                        for ip in device.ips:
                            # cchen: ip.version is a enum so we have to use "value" to
                            # get its real value we are assuming that only the IP which
                            # starts with '10' is something that we are interested in
                            if ip.version.value == 'v4' and ip.address.startswith('10'):
                                addr += ip.address + '  '
                rows.append([vm.id, vm.name, vm.status.value.upper(), addr, comment])
            output = Output(["ID", "Name", "Status", "Networks", "Comment"], rows)
            output.print_table()
            self.c.close()
        except sdk.Error as err:
            print "Failed to list VMs, %s" % str(err)

    def vm_start(self, args):
        vms_services = self.c.system_service().vms_service()
        search_prefix = 'name=' + args.vm_name
        try:
            vm = vms_services.list(search=search_prefix)[0]
            vm_service = vms_services.vm_service(vm.id)
            vm_service.start()
            self.c.close()
        except sdk.Error as err:
            print ("Failed to start %s, %s" % (args.vm_name, str(err)))
        except IndexError:
            print "Error: No such VM %s" % args.vm_name
        else:
            print "The request of starting %s has been sent" % vm.name

    def vm_stop(self, args):
        c_obj = Connect()
        c = c_obj.connect()
        vms_service = c.system_service().vms_service()
        search_prefix = 'name=' + args.vm_name
        try:
            vm = vms_service.list(search=search_prefix)[0]
            vm_service = vms_service.vm_service(vm.id)
            vm_service.stop()
            self.c.close()
        except sdk.Error as err:
            print ("Failed to stop %s, %s" % (args.vm_name, str(err)))
        except IndexError:
            print "Error: No such VM %s" % args.vm_name
        else:
            print "The request of stopping %s has been sent" % vm.name

    def vm_delete(self, args):
        vms_service = self.c.system_service().vms_service()
        search_prefix = 'name=' + args.vm_name
        try:
            vm = vms_service.list(search=search_prefix)[0]
            vm_service = vms_service.vm_service(vm.id)
            vm_service.remove()
            self.c.close()
        except sdk.Error as err:
            print ("Failed to delete %s, %s" % (args.vm_name, str(err)))
        except IndexError:
            print "Error: No such VM %s" % args.vm_name
        else:
            print "The request of deleting %s has been sent" % vm.name

    def vm_boot(self, args):
        vms_service = self.c.system_service().vms_service()
        if args.vm_raw == '1':
            template_used = 'Blank'
        else:
            template_used = args.temp
        try:
            vm = vms_service.add(
                types.Vm(
                    name=args.vm_name,
                    cluster=types.Cluster(
                        # A little bit dangerous as we hardcoded the cluster name as 'Default'
                        name='Default',
                    ),
                    template=types.Template(
                        name=template_used,
                    ),
                    comment=args.vm_comment,
                ),
            )
            self.c.close()
        except sdk.Error as err:
            print ("%s creation failed, %s" % (args.vm_name, str(err)))
        else:
            print "The request of creating %s has been sent." % vm.name

    def vm_console(self, args):
        vms_service = self.c.system_service().vms_service()
        search_prefix = 'name=' + args.vm_name
        try:
            vm = vms_service.list(search=search_prefix)[0]
            vm_service = vms_service.vm_service(vm.id)
            consoles_service = vm_service.graphics_consoles_service()
            consoles = consoles_service.list(current=True)
            console = next(
                (c for c in consoles if c.protocol == types.GraphicsType.VNC),
                None
            )
            if console is not None:
                # cchen: VNC found and usually we use VNC for our VM display because spice doesn't
                # work sometimes
                console_service = consoles_service.console_service(console.id)
                # cchen: If the password contains "/" then the console can not be opened.
                while 1:
                    ticket = console_service.ticket()
                    if "/" not in ticket.value:
                        break
                try:
                    vnc_url = "vnc://:%s@%s:%d" % (ticket.value, console.address, console.port)
                    if environ.get('TITAMU_DIST') == 'MacOS':
                        # For MacOS we simply let OS open the VNC url.
                        # TODO: Linux to be implemented
                        subprocess.call(["/usr/bin/open", vnc_url])
                except IOError as ioerr:
                    print "Can not open console.vv %s" % str(ioerr)
            elif console is None:
                # VNC didn't find so the console might be spice
                console = next(
                    (c for c in consoles if c.protocol == types.GraphicsType.SPICE),
                    None
                )
                if console is not None:
                    console_service = consoles_service.console_service(console.id)
                    # cchen: Simply call the remote_viewer_connection_file function to get console.vv
                    console_vv = console_service.remote_viewer_connection_file()
                    path = "/tmp/console.vv"
                    with open(path, "w") as f:
                        f.write(console_vv)
                    try:
                        if environ.get('TITAMU_DIST') == 'MacOS':
                            # TODO: Linux to be implemented the same as VNC
                            subprocess.call('remote-viewer /tmp/console.vv 2>/dev/null', shell=True)
                    except OSError as err:
                        print "Unable to locate remote-viewer application: %s" % err

            self.c.close()
        except sdk.Error as err:
            print str(err)
        except IndexError:
            print "Error: No such VM %s" % args.vm_name

    def vm_show(self, args):
        vms_service = self.c.system_service().vms_service()
        try:
            rows = []

            vm = vms_service.list(search=args.vm_name)[0]
            vm_service = vms_service.vm_service(vm.id)
            # Print basic information
            rows.append(["Name", vm.name])
            rows.append(["ID", vm.id])
            rows.append(["Status", str(vm.status).upper()])
            rows.append(["Memory", str(vm.memory / 1024 / 1024)+'M'])
            rows.append(["CPU", vm.cpu.topology.cores * vm.cpu.topology.sockets * vm.cpu.topology.threads])
            # Print Disk information
            disk_attachments_service = vm_service.disk_attachments_service()
            disk_attachments = disk_attachments_service.list()
            for disk_attachment in disk_attachments:
                disk = self.c.follow_link(disk_attachment.disk)
                rows.append(["Disks",[disk.name, disk.id, str(disk.provisioned_size/1024/1024/1024)+'G']])

            # We use nics_service() instead of reported_devices_service()
            # because we need to get NIC id and name
            nics_service = vm_service.nics_service().list()
            for nic in nics_service:
                for device in nic.reported_devices:
                    if device.ips is not None:
                        for ip in device.ips:
                            if ip.version.value == 'v4':
                                rows.append(["Active Nics", [nic.name, nic.mac.address, nic.id, ip.address]])
                    if device.ips is None:
                        rows.append(["Inactive Nics", [nic.name, nic.mac.address, nic.id]])

            output = Output(["Item", "Value"], rows)
            output.print_table()
        except sdk.Error as err:
            print str(err)
        except IndexError:
            print "Error: No such VM %s" % args.vm_name
