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
        pillar = task_vars.get('pillar', {})
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
            facts[k] = choice_map.get(func_type)(myhost, v, **args)
        result['failed'] = False
        pillar.update(facts)
        result['ansible_facts'] = {'pillar': pillar}
        result['changed'] = False
        return result
