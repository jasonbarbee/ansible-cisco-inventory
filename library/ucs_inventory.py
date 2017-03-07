#!/usr/bin/python


ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'jasonbarbee',
                    'version': '0.1'}


DOCUMENTATION = '''
---
module: ucs_inventory
version_added: "2.2"
short_description: Inventory Report module
description:
    - Pulls model and serials for a UCS System.
author: Jason Barbee (@jasonbarbee)
extends_documentation_fragment: ucs
options:
    output_file: - path and filename of CSV export.
    Writes a static ucs.csv file to the ansible folder with serials for mydevices.
'''

EXAMPLES = '''
- name: Pull UCS Inventory {{ucsm_ip}}
      ucs_inventory:
        ip={{ucsm_ip}}
        login={{ucsm_login}}
        password={{ucsm_pw}}
'''

from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider
from library.ucs import UCS
import csv
import sys

def ucs_inventory(module):
    ucsm_ip = module.params.get('ip')
    ucsm_pw = module.params.get('password')
    ucsm_login = module.params.get('login')

    ucsm = UCS(ucsm_ip, ucsm_login, ucsm_pw)

    results = {}

    #Login to UCSM
    try:
        ucsm.login()
        results['logged_in'] = True
    except Exception as e:
        module.fail_json(msg=e)

    query_dict = {}
    query_dict['chassis'] = {}
    query_dict['fi'] = {}
    query_dict['blade'] = {}

    try:
        query_data = ucsm.handle.query_classids('orgOrg', 'EquipmentChassis', 'NetworkElement', 'ComputeBlade')
        with open(module.params.get('output_file'),'w+') as ucs_file:
                writer = csv.writer(ucs_file)
                writer.writerow(['Serial Number','Device Name / Hostname','Tags','Notes'])
                for chassis in query_data['EquipmentChassis']:
                    query_dict['chassis'][chassis.dn] = {}
                    query_dict['chassis'][chassis.dn]['model'] = chassis.model
                    query_dict['chassis'][chassis.dn]['serial'] = chassis.serial
                    writer.writerow([chassis.serial,ucsm_ip,'UCS-Chassis',''])

                for fi in query_data['NetworkElement']:
                    query_dict['fi'][fi.dn] = {}
                    query_dict['fi'][fi.dn]['model'] = fi.model
                    query_dict['fi'][fi.dn]['serial'] = fi.serial
                    writer.writerow([fi.serial,ucsm_ip,'UCS-FI',''])

                for blade in query_data['ComputeBlade']:
                    query_dict['blade'][blade.dn] = {}
                    query_dict['blade'][blade.dn]['model'] = blade.model
                    query_dict['blade'][blade.dn]['serial'] = blade.serial
                    writer.writerow([blade.serial,ucsm_ip,'UCS-Blades',''])

    except Exception as e:
        module.fail_json(msg=e)

    try:
        ucsm.handle.logout()
        results['logged_out'] = True
    except Exception as e:
        module.fail_json(msg=e)
    results['inventory'] = query_dict
    return results

def main():
    module = AnsibleModule(
        argument_spec     = dict(
        ip                = dict(required=True),
        password          = dict(required=True),
        login             = dict(required=True),
        )
    )

    results = ucs_inventory(module)
    module.exit_json(**results)



from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
