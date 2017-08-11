#!/usr/bin/python

import pypillar.utils

DOCUMENTATION = '''
---
module: get_setting
short_description: get setting from salt pillar
'''

EXAMPLES = '''
- name: get setting
  get_setting:
    myhost: "{{ myhost.meta }}"
    setting: "{{ mysql_daemon }}"
    extra_setting: {'check_osver': True }
    value_type: dict
  register: mysql_daemon
  ignore_errors: true
'''

def main():

    fields = {
        "myhost": {"required": True, "type": "dict"},
        "setting": {"required": True, "type": "dict"},
        "extra_setting": {"default": {}, "type": "dict"},
        "value_type": {
          "default": "dict",
          "choices": ["dict", "list"],
          "type": "str"
        },
    }

    choice_map = {
        "dict": get_setting_dict,
        "list": get_setting_list,
    }

    module = AnsibleModule(argument_spec=fields)
    result = choice_map.get(module.params['value_type'])(module.params['myhost'], module.params['setting'], **module.params['extra_setting'])
    module.exit_json(meta=result)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()

