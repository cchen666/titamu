import ovirtsdk4 as sdk
from os import environ
from prettytable import PrettyTable


class Connect:
    def __init__(self):
        # Sample environment variables that you should set
        # export TITAN_URL='https://lab-rhevm.microsoft.rdu.com/ovirt-engine/api'
        # export TITAN_USERNAME='adminuser@your_domain'
        # export TITAN_PASSWORD='password'
        # export TITAN_CA_FILE='ca.pem'
        # export TITAN_VM_PREFIX='your_user'
        # export TITAN_DEFAULT_TEMPLATE='your_preferred_template'
        env_dict = environ
        self.url = env_dict.get('TITAN_URL')
        self.username = env_dict.get('TITAN_USERNAME')
        self.password = env_dict.get('TITAN_PASSWORD')
        self.ca_file = env_dict.get('TITAN_CA_FILE')
        self.debug = True

    def connect(self):
        return sdk.Connection(url=self.url,
                              username=self.username,
                              password=self.password,
                              ca_file=self.ca_file,
                              debug=self.debug)


class Output:
    # A class that uses pretty table to output. It needs two parameters:
    # fields: table column
    # rows: the actual values that fills the table
    def __init__(self, fields, rows):
        self.pt = PrettyTable()
        self.pt.field_names = fields
        self.rows = rows
        self.pt.align = 'l'

    def print_table(self):
        for row in self.rows:
            self.pt.add_row(row)
        print self.pt


class Help:
    def __init__(self):
        self.help_message = '''usage: titamu [-h] {start,test,stop,show,delete,list,boot,console,sd-list,net-list,net-add,
        net-rm,disk-list,disk-add,temp-list} ...

positional arguments:
  {start,test,stop,show,delete,list,boot,console,sd-list,net-list,net-add,net-rm,disk-list,disk-add,temp-list}

optional arguments:
  -h, --help            show this help message and exit
'''

    def print_help(self):
        print self.help_message
