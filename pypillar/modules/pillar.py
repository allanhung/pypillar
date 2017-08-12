#!/usr/bin/python

DOCUMENTATION = '''
---
module: pillar
short_description: set variable to pillar
'''

EXAMPLES = '''
- name:
  pillar: {}
'''

def main():
    fields = {}
    module = AnsibleModule(argument_spec=fields)
    module.exit_json(changed=False)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
