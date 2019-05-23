import ovirtsdk4 as sdk
import ovirtsdk4.types as types

from utils import Connect
from utils import Output


class StorageDomainOps:
    def __init__(self):
        self.connect = Connect()
        self.c = self.connect.connect()

    def sd_list(self, args):
        try:
            sds_service = self.c.system_service().storage_domains_service()
            rows = []
            for sd in sds_service.list():
                if sd.available is not None and sd.used is not None:
                    rows.append([sd.id,
                                 sd.name,
                                 sd.storage.type,
                                 str((sd.available + sd.used) / 1024 / 1024 / 1024) + 'G',
                                 str(sd.available / 1024 / 1024 / 1024) + 'G'])
                else:
                    rows.append([sd.id,
                                 sd.name,
                                 sd.storage.type,
                                 "N/A",
                                 "N/A"])
            output = Output(["ID", "Name", "Type", "Total", "Free"], rows)
            output.print_table()
        except sdk.Error as err:
            print "Failed to list disks, %s" % str(err)

    def sd_optimize(self, args):
        # TODO: Compare args.request_size and free size for each SD
        # TODO: return: First SD id that meets args.request_size
        pass
