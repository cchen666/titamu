import pytest
from titamu.tests.utils import *

ENV_TITANRC = '/Users/cchen/.bash_profile'
ENV_TEST_VM_NAME = "cchen-tox-" + gen_random(5, 0, 9)

class TestVM:
    def setup(self):
        print("Setup")

    def teardown(self):
        print("teardown")

    def test_vm_list(self):
        test_command = "source " + ENV_TITANRC + ";" + "titamu list 2>/dev/null"
        r = commands.getstatusoutput(test_command)[0]
        assert r == 0, test_command

    def test_vm_boot(self):
        test_command = "source " + ENV_TITANRC + ";" + "titamu boot " + ENV_TEST_VM_NAME + " 2>/dev/null"
        r = commands.getstatusoutput(test_command)[0]
        assert r == 0, test_command
        test_command = "source " + ENV_TITANRC + ";" + "titamu list | grep " + ENV_TEST_VM_NAME + " | awk '{print $6}'"
        r = loop_check(test_command, 5, 10, "DOWN")
        assert r == 0, test_command

    def test_vm_start(self):
        test_command = "source " + ENV_TITANRC + ";" + "titamu start " + ENV_TEST_VM_NAME + " 2>/dev/null"
        r = commands.getstatusoutput(test_command)[0]
        assert r == 0, test_command
        test_command = "source " + ENV_TITANRC + ";" + "titamu list | grep " + ENV_TEST_VM_NAME + " | awk '{print $6}'"
        r = loop_check(test_command, 5, 10, "UP")
        assert r == 0, test_command
        # TODO: Ping the VM

    def test_vm_show(self):
        test_command = "source " + ENV_TITANRC + ";" + "titamu show " + ENV_TEST_VM_NAME + " 2>/dev/null"
        r = commands.getstatusoutput(test_command)[0]
        assert r == 0, test_command

    def test_vm_stop(self):
        test_command = "source " + ENV_TITANRC + ";" + "titamu stop " + ENV_TEST_VM_NAME + " 2>/dev/null"
        r = commands.getstatusoutput(test_command)[0]
        assert r == 0, test_command
        test_command = "source " + ENV_TITANRC + ";" + "titamu list | grep " + ENV_TEST_VM_NAME + " | awk '{print $6}'"
        r = loop_check(test_command, 5, 10, "DOWN")
        assert r == 0, test_command

    def test_vm_delete(self):
        test_command = "source " + ENV_TITANRC + ";" + "titamu delete " + ENV_TEST_VM_NAME + " 2>/dev/null"
        r = commands.getstatusoutput(test_command)[0]
        assert r == 0, test_command
        test_command = "source " + ENV_TITANRC + ";" + "titamu list | grep " + ENV_TEST_VM_NAME + " | wc -l"
        r = loop_check(test_command, 5, 10, '0')
        assert r == 0, test_command
