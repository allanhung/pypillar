from ansible.plugins.action import ActionBase
from pypillar.utils import *

class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        facts = {}
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        if result.get('skipped'):
            return result

        # parser host
        inventory_hostname = task_vars.get('inventory_hostname', '')
        ansible_distribution = task_vars.get('ansible_distribution', '')
        ansible_distribution_version = task_vars.get('ansible_distribution_version', '')
        myhost = get_host.parser_host(inventory_hostname, ansible_distribution, ansible_distribution_version)
        facts['myhost']=myhost
        # process pillar
        pillar = task_vars.get('pillar', {})
        choice_map = {
            "dict": get_setting.get_dict,
            "list": get_setting.get_list,
        }     
        for k, v in pillar.items():
            self._display.v('parse setting: {}'.format(str(k)))
            args=v.pop('args', {})
            func_type=args.pop('type', 'dict')
            check_osver=args.get('check_osver', False)
            if 'default' in list(v.keys()):
                if check_osver:
                    func_type='dict' if isinstance(v['default'].values()[0], dict) else 'list'
                else:
                    func_type='dict' if isinstance(v['default'], dict) else 'list'
            elif 'example' in list(v.keys()):
                if check_osver:
                    func_type='dict' if isinstance(v['example'].values()[0], dict) else 'list'
                else:
                    func_type='dict' if isinstance(v['example'], dict) else 'list'
            else:
                if check_osver:
                    func_type='dict' if isinstance(v[list(v.keys())[0]].values()[0], dict) else 'list'
                else:
                    func_type='dict' if isinstance(v[list(v.keys())[0]], dict) else 'list'
            facts[k] = choice_map.get(func_type)(myhost, v, **args)
        result['failed'] = False
        pillar.update(facts)
        result['ansible_facts'] = {'pillar': pillar}
        result['changed'] = False
        return result
