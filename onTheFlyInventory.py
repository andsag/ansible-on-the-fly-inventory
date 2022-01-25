#!/usr/bin/env python3

'''
Temporary inventory script for Ansible, in Python. Script create inventory based
on environment variable INVENTORY_HOSTS.
Example:
export INVENTORY_HOSTS="192.168.1.2, 192.168.1.3"
'''

import os
from shlex import shlex
import sys
import argparse
import json

class tempInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        if self.args.list:
            INVENTORY_HOSTS = os.getenv('INVENTORY_HOSTS')
            if not INVENTORY_HOSTS:
                self.inventory = self.empty_inventory()
            else:
                self.inventory = self.temp_inventory(INVENTORY_HOSTS)
        else:
            self.inventory = self.empty_inventory()

        print(json.dumps(self.inventory));

    def temp_inventory(self,INVENTORY_HOSTS):
        json_string = """
        {
            "_meta": {
                "hostvars": {}
            },
            "windows" : {
                "hosts" : [],
                "vars": {
                    "ansible_connection": "winrm",
                    "ansible_port": "5985",
                    "ansible_winrm_transport": "ntlm",
                    "ansible_winrm_server_cert_validation": "ignore"
                }
            }
        }
        """
        data = json.loads(json_string)
        data["windows"]["hosts"] += INVENTORY_HOSTS.replace(" ", "").split(',')
        return data

    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        self.args = parser.parse_args()

tempInventory()
