#!/usr/bin/python

DOCUMENTATION = '''
---
module: get_host
short_description: parser host information
'''

EXAMPLES = '''
- name: get host
  get_host:
    hostname: "{{ inventory_hostname }}"
    osdist: "{{ ansible_distribution }}"
    osver: "{{ ansible_distribution_version }}"
  register: myhost
  ignore_errors: true
'''

KEY_PREFIX='my_'

def parser_myhost(hostname, osdistribution, osver):
    """
    set host attr by os version, hostname

    os_ver: 
      Microsoft Windows Server 2012 R2 Standard: 6.3.9600.0

    """
    results = {}
    host, domain = hostname.split('.',1)
    os_ver_list = osver.split('.')
    if 'windows' in osdistribution.lower():
        domain = host[:4]
        results[KEY_PREFIX+'os_ver'] = os_ver_list[0]+'.'+os_ver_list[1]
        results[KEY_PREFIX+'os_subver'] = os_ver_list[2]+'.'+os_ver_list[3]
    elif 'centos' in osdistribution.lower():
      results[KEY_PREFIX+'os_ver'] = os_ver_list[0]
      results[KEY_PREFIX+'os_subver'] = os_ver_list[0]+'.'+os_ver_list[1]
    else:
      results[KEY_PREFIX+'os_ver'] = os_ver_list[0]
      results[KEY_PREFIX+'os_subver'] = os_ver_list[0]+'.'+os_ver_list[1]
    results[KEY_PREFIX+'hostname'] = host.lower()
    results[KEY_PREFIX+'domain'] = domain.lower()
    return results

def main():

    fields = {
        "hostname": {"required": True, "type": "str"},
        "osdist": {"required": True, "type": "str"},
        "osver": {"required": True, "type": "str"},
    }

    module = AnsibleModule(argument_spec=fields)
    myhost = parser_myhost(module.params['hostname'], module.params['osdist'], module.params['osver'])
    module.exit_json(**myhost)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
