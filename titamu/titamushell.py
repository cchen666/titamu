import argparse
from template import TempOps
from vm import VmOps
from net import NetOps
from disk import DiskOps
from storagedomain import StorageDomainOps
from utils import Help

from os import environ
from sys import argv


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser')

    if argv[1].startswith('temp'):
        # Every operations that are related to template must start with "temp"
        tempops = TempOps()
        parser_templist = subparsers.add_parser('temp-list')
        parser_templist.add_argument('-p', '--prefix', default=environ.get("TITAMU_PREFIX"), dest='prefix')
        parser_templist.set_defaults(func=tempops.temp_list)

    elif argv[1].startswith('net'):
        # Every operations that are related to networks must start with "net"
        netops = NetOps()
        parser_netlist = subparsers.add_parser('net-list')
        parser_netlist.set_defaults(func=netops.net_list)

        parser_netadd = subparsers.add_parser('net-add')
        parser_netadd.add_argument('-n', '--network', dest='net_id')
        parser_netadd.add_argument('vm_name')
        parser_netadd.set_defaults(func=netops.net_add)

        parser_netadd = subparsers.add_parser('net-rm')
        parser_netadd.add_argument('-p', '--port', dest='port_id')
        parser_netadd.add_argument('vm_name')
        parser_netadd.set_defaults(func=netops.net_rm)

    elif argv[1].startswith('disk'):
        diskops = DiskOps()
        parser_disklist = subparsers.add_parser('disk-list')
        parser_disklist.add_argument('-p', '--prefix', default=environ.get("TITAMU_PREFIX"), dest='prefix')
        parser_disklist.add_argument('vm_name')
        parser_disklist.set_defaults(func=diskops.disk_list)

    elif argv[1].startswith('sd'):
        sdops = StorageDomainOps()
        parser_disklist = subparsers.add_parser('sd-list')
        parser_disklist.set_defaults(func=sdops.sd_list)

    elif argv[1].startswith('-h') or argv[1].startswith('--help') or argv[1].startswith('help'):
        help = Help()
        parser_help = subparsers.add_parser('-blabla')
        parser_help.set_defaults(func=help.print_help())

    else:
        vmops = VmOps()
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='subparser')

        parser_start = subparsers.add_parser('start')
        parser_start.add_argument('vm_name', help='Alpha description')
        parser_start.set_defaults(func=vmops.vm_start)

        # test
        parser_test = subparsers.add_parser('test')
        parser_test.add_argument('-p', '--prefix', default=environ.get("TITAMU_PREFIX"), dest='prefix')
        parser_test.set_defaults(func=vmops.vm_list)
        # test

        parser_stop = subparsers.add_parser('stop')
        parser_stop.add_argument('vm_name')
        parser_stop.set_defaults(func=vmops.vm_stop)

        parser_show = subparsers.add_parser('show')
        parser_show.add_argument('vm_name')
        parser_show.set_defaults(func=vmops.vm_show)

        parser_stop = subparsers.add_parser('delete')
        parser_stop.add_argument('vm_name')
        parser_stop.set_defaults(func=vmops.vm_delete)

        parser_list = subparsers.add_parser('list')
        parser_list.add_argument('-p', '--prefix', default=environ.get("TITAMU_PREFIX"), dest='prefix')
        parser_list.set_defaults(func=vmops.vm_list)

        parser_boot = subparsers.add_parser('boot')
        parser_boot.add_argument('-t', '--template', default=environ.get("TITAMU_DEFAULT_TEMPLATE"), dest='temp')
        parser_boot.add_argument('-c', '--comment', dest='vm_comment')
        parser_boot.add_argument('-r', '--raw', default='0', dest='vm_raw')
        parser_boot.add_argument('vm_name')
        parser_boot.set_defaults(func=vmops.vm_boot)

        parser_console = subparsers.add_parser('console')
        parser_console.add_argument('vm_name')
        parser_console.set_defaults(func=vmops.vm_console)

    args = parser.parse_args(argv[1:])
    args.func(args)


if __name__ == "__main__":
    main()
