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
            check_osver=args.get('check_osver', False)
            if 'default' in v.keys():
                if check_osver:
                    # default:
                    #   7:
                    #     key1: value1
                    func_type='dict' if isinstance(v['default'].values()[0], dict) else 'list'
                else:
                    # default:
                    #   key1: value1
                    func_type='dict' if isinstance(v['default'], dict) else 'list'
            elif 'example' in v.keys():
                if check_osver:
                    func_type='dict' if isinstance(v['example'].values()[0], dict) else 'list'
                else:
                    func_type='dict' if isinstance(v['example'], dict) else 'list'
            else:
                if check_osver:
                    # domain:
                    #   domain1:
                    #     7:
                    #       key1: value1
                    self._display.v('pillar value 0 with check osver: {}'.format(v.values()[0].values()[0]))
                    func_type='dict' if isinstance(v.values()[0].values()[0].values()[0], dict) else 'list'
                else:
                    # domain:
                    #   domain1:
                    #     key1: value1
                    self._display.v('pillar value 0: {}'.format(v.values()[0].values()[0]))
                    func_type='dict' if isinstance(v.values()[0].values()[0], dict) else 'list'
            self._display.v('function type: {}'.format(func_type))
            facts[k] = choice_map.get(func_type)(myhost, v, **args)
        result['failed'] = False
        pillar.update(facts)
        result['ansible_facts'] = {'pillar': pillar}
        result['changed'] = False
        return result
