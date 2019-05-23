import ovirtsdk4 as sdk
import sys
from os import environ
from prettytable import PrettyTable


class Connect:
    def __init__(self):
        # Sample environment variables that you should set
        # export TITAMU_URL='https://lab-rhevm.microsoft.rdu.com/ovirt-engine/api'
        # export TITAMU_USERNAME='adminuser@your_domain'
        # export TITAMU_PASSWORD='password'
        # export TITAMU_CA_FILE='ca.pem'
        # export TITAMU_VM_PREFIX='your_user'
        # export TITAMU_DEFAULT_TEMPLATE='your_preferred_template'
        env_dict = environ
        self.url = env_dict.get('TITAMU_URL')
        self.username = env_dict.get('TITAMU_USERNAME')
        self.password = env_dict.get('TITAMU_PASSWORD')
        self.ca_file = env_dict.get('TITAMU_CA_FILE')
        self.debug = True
        if self.url == '' or self.username == '' or self.password == '' or self.ca_file == '':
            messages = '''
Please make sure you set TITAMU environment variables in your bash profile
export TITAMU_URL=<RHV URL>
export TITAMU_USERNAME=<username>@<domainname>
export TITAMU_PASSWORD=<password>
export TITAMU_CA_FILE=<RHV CA FILE>
export TITAMU_DEFAULT_TEMPLATE=<Your preferred template>
export TITAMU_VM_PREFIX=<Usually your krb5 username>
'''
            print messages
            sys.exit(1)

    def connect(self):
        return sdk.Connection(url=self.url,
                              username=self.username,
                              password=self.password,
                              ca_file=self.ca_file,
                              debug=self.debug)


class Output:
    # A class that uses pretty table to output. It needs two parameters:
    # fields: table column - 1-dimension list
    # rows: the actual values that fills the table - 2-dimension list
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
