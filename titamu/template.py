from utils import Connect
from utils import Output


class TempOps:
    def __init__(self):
        self.connect = Connect()
        self.c = self.connect.connect()

    def temp_list(self, args):
        templates_service = self.c.system_service().templates_service()
        try:
            if args.prefix is not None:
                search_prefix = 'name=' + args.prefix + '*'
            else:
                search_prefix = '*'
            templates = templates_service.list(search=search_prefix)
            rows = []
            for template in templates:
                cores = template.cpu.topology.cores * template.cpu.topology.sockets * template.cpu.topology.threads
                memory = template.memory / 1024 / 1024
                description = ""
                if template.description is not None:
                    description = template.description
                rows.append([template.id, template.name, str(memory) + ' M', cores, str(description)])
            output = Output(["ID", "Name", "Mem", "CPU", "Description"], rows)
            output.print_table()
            self.c.close()
        except sdk.Error as err:
            print "Failed to list templates, %s" % str(err)
