#!/usr/bin/python

DOCUMENTATION = '''
---
module: get_setting
short_description: get setting from salt pillar
'''

from copy import deepcopy

SETTING_LIST = ['domain', 'hostname']

def get_host_dict(myhost, root_value, config_key, kwargs):
    check_osver=kwargs.get('check_osver',False)
    # domain replace
    if 'domain' in kwargs.keys():
        mydomain = kwargs['domain']
    else:
        mydomain = myhost['domain']
    # set host_config_key
    if config_key == 'domain':
        host_config_key = mydomain
    elif config_key == 'hostport':
        host_config_key = myhost['hostname']+':'+str(kwargs.get('port',0))
    else:
        host_config_key = myhost[config_key]

    context_host={}
    if check_osver:
        if not context_host:
            # key:
            #   config_key.domain:
            #     os_ver:
            #       myhost[config_key]
            context_host.update(root_value.get(config_key+'.'+mydomain,{}).get(myhost['os_ver'],{}).get(host_config_key,{}))
            # key:
            #   config_key.domain:
            #     os_subver:
            #       myhost[config_key]
            context_host.update(root_value.get(config_key+'.'+mydomain,{}).get(myhost['os_subver'],{}).get(host_config_key,{}))
        if not context_host:
            # key:
            #   config_key:
            #     os_ver:
            #       myhost[config_key].domain
            context_host.update(root_value.get(config_key,{}).get(myhost['os_ver'],{}).get(host_config_key+'.'+mydomain,{}))
            # key:
            #   config_key:
            #     os_subver:
            #       myhost[config_key].domain
            context_host.update(root_value.get(config_key,{}).get(myhost['os_subver'],{}).get(host_config_key+'.'+mydomain,{}))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key].domain
            #       os_ver:
            context_host.update(root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,{}).get(myhost['os_ver'],{}))
            # key:
            #   config_key:
            #     myhost[config_key].domain
            #       os_subver:
            context_host.update(root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,{}).get(myhost['os_subver'],{}))
        if not context_host:
            # key:
            #   config_key:
            #     os_ver:
            #       myhost[config_key]
            context_host.update(root_value.get(config_key,{}).get(myhost['os_ver'],{}).get(host_config_key,{}))
            # key:
            #   config_key:
            #     os_subver:
            #       myhost[config_key]
            context_host.update(root_value.get(config_key,{}).get(myhost['os_subver'],{}).get(host_config_key,{}))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key]
            #       os_ver:
            context_host.update(root_value.get(config_key,{}).get(host_config_key,{}).get(myhost['os_ver'],{}))
            # key:
            #   config_key:
            #     myhost[config_key]
            #       os_subver:
            context_host.update(root_value.get(config_key,{}).get(host_config_key,{}).get(myhost['os_subver'],{}))
        # process with default_os
        if not context_host:
            # key:
            #   config_key.domain:
            #     defualt_os:
            #       myhost[config_key]
            context_host.update(root_value.get(config_key+'.'+mydomain,{}).get('default_os',{}).get(host_config_key,{}))
        if not context_host:
            # key:
            #   config_key:
            #     defualt_os:
            #       myhost[config_key].domain
            context_host.update(root_value.get(config_key,{}).get('default_os',{}).get(host_config_key+'.'+mydomain,{}))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key].domain
            #       defualt_os
            context_host.update(root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,{}).get('default_os',{}))
        if not context_host:
            # key:
            #   config_key:
            #     defualt_os:
            #       myhost[config_key]
            context_host.update(root_value.get(config_key,{}).get('default_os',{}).get(host_config_key,{}))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key]
            #       defualt_os
            context_host.update(root_value.get(config_key,{}).get(host_config_key,{}).get('default_os',{}))
    else:
        if not context_host:
            # key:
            #   config_key.domain:
            #     myhost[config_key]
            context_host.update(root_value.get(config_key+'.'+mydomain,{}).get(host_config_key,{}))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key].domain
            context_host.update(root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,{}))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key]
            context_host.update(root_value.get(config_key,{}).get(host_config_key,{}))
    return context_host

def join_dict(dictx, dicty, merge_list=False):
    dicta=deepcopy(dictx)
    dictb=deepcopy(dicty)
    for k, v in dictb.iteritems():
        if isinstance(v, dict):
            if k in dicta.keys():
                if isinstance(dicta[k], dict):
                    dicta[k].update(join_dict(dicta[k], v))
                else:
                    dicta[k].update(v)
            else:
                dicta[k]=v
        elif merge_list and isinstance(v, list):
            if k in dicta.keys():
                dicta[k].extend(v)
            else:
                dicta[k]=v
        else:
            dicta[k]=v            
    return dicta

def get_dict(myhost, setting, **kwargs):
    default=kwargs.get('default','all')
    merge_list=kwargs.get('merge_list',False)
    check_osver=kwargs.get('check_osver',False)
    context={}
    root_value=setting
    # get default
    context['default']={}
    if check_osver:
        if not context['default']:
            # key:
            #   default:
            #     os_ver:
            context['default'].update(root_value.get('default',{}).get(myhost['os_ver'],{}))
            # key:
            #   default:
            #     subos_ver:
            context['default'].update(root_value.get('default',{}).get(myhost['os_subver'],{}))
        if not context['default']:
            # key:
            #   default:
            #     default_os:
            context['default'].update(root_value.get('default',{}).get('default_os',{}))
    else:
        # key:
        #   default:
        context['default'].update(root_value.get('default',{}))
    if default == 'all':
        for attr in SETTING_LIST:           
            context[attr]=get_host_dict(myhost, root_value, attr, kwargs)
            context['default']=join_dict(context['default'], context[attr], merge_list)
        return context['default']
    else:
        for attr in reversed(SETTING_LIST):
            context[attr]=get_host_dict(myhost, root_value, attr, kwargs)
            if context[attr]:
                return context[attr]
        return context['default']

def get_host_list(myhost, root_value, config_key, kwargs):
    merge_dict=kwargs.get('merge_dict',True)
    check_osver=kwargs.get('check_osver',False)
    # domain replace
    if 'domain' in kwargs.keys():
        mydomain = kwargs['domain']
    else:
        mydomain = myhost['domain']
    # set host_config_key
    if config_key == 'domain':
        host_config_key = mydomain
    elif config_key == 'hostport':
        host_config_key = myhost['hostname']+'_'+str(kwargs.get('port',0))
    else:
        host_config_key = myhost[config_key]

    context_host=[]
    if check_osver:
        if not context_host:
            # key:
            #   config_key.domain:
            #     os_ver:
            #       myhost[config_key]
            context_host.extend(root_value.get(config_key+'.'+mydomain,{}).get(myhost['os_ver'],{}).get(host_config_key,[]))
            # key:
            #   config_key.domain:
            #     os_subver:
            #       myhost[config_key]
            context_host=join_list(context_host, root_value.get(config_key+'.'+mydomain,{}).get(myhost['os_subver'],{}).get(host_config_key,[]),merge_dict)
        if not context_host:
            # key:
            #   config_key:
            #     os_ver:
            #       myhost[config_key].domain
            context_host.extend(root_value.get(config_key,{}).get(myhost['os_ver'],{}).get(host_config_key+'.'+mydomain,[]))
            # key:
            #   config_key:
            #     os_subver:
            #       myhost[config_key].domain
            context_host=join_list(context_host, root_value.get(config_key,{}).get(myhost['os_subver'],{}).get(host_config_key+'.'+mydomain,[]),merge_dict)
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key].domain
            #       os_ver:
            context_host.extend(root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,{}).get(myhost['os_ver'],[]))
            # key:
            #   config_key:
            #     myhost[config_key].domain
            #       os_subver:
            context_host=join_list(context_host, root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,{}).get(myhost['os_subver'],[]),merge_dict)
        if not context_host:
            # key:
            #   config_key:
            #     os_ver:
            #       myhost[config_key]
            context_host.extend(root_value.get(config_key,{}).get(myhost['os_ver'],{}).get(host_config_key,[]))
            # key:
            #   config_key:
            #     os_subver:
            #       myhost[config_key]
            context_host=join_list(context_host, root_value.get(config_key,{}).get(myhost['os_subver'],{}).get(host_config_key,[]),merge_dict)
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key]
            #       os_ver:
            context_host.extend(root_value.get(config_key,{}).get(host_config_key,{}).get(myhost['os_ver'],[]))
            # key:
            #   config_key:
            #     myhost[config_key]
            #       os_subver:
            context_host=join_list(context_host, root_value.get(config_key,{}).get(host_config_key,{}).get(myhost['os_subver'],[]),merge_dict)
        # process with default_os
        if not context_host:
            # key:
            #   config_key.domain:
            #     defualt_os:
            #       myhost[config_key]
            context_host.extend(root_value.get(config_key+'.'+mydomain,{}).get('default_os',{}).get(host_config_key,[]))
        if not context_host:
            # key:
            #   config_key:
            #     defualt_os:
            #       myhost[config_key].domain
            context_host.extend(root_value.get(config_key,{}).get('default_os',{}).get(host_config_key+'.'+mydomain,[]))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key].domain
            #       defualt_os
            context_host.extend(root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,{}).get('default_os',[]))
        if not context_host:
            # key:
            #   config_key:
            #     defualt_os:
            #       myhost[config_key]
            context_host.extend(root_value.get(config_key,{}).get('default_os',{}).get(host_config_key,[]))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key]
            #       defualt_os
            context_host.extend(root_value.get(config_key,{}).get(host_config_key,{}).get('default_os',[]))
    else:
        if not context_host:
            # key:
            #   config_key.domain:
            #     myhost[config_key]
            context_host.extend(root_value.get(config_key+'.'+mydomain,{}).get(host_config_key,[]))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key].domain
            context_host.extend(root_value.get(config_key,{}).get(host_config_key+'.'+mydomain,[]))
        if not context_host:
            # key:
            #   config_key:
            #     myhost[config_key]
            context_host.extend(root_value.get(config_key,{}).get(host_config_key,[]))
    return context_host

def join_list(lista, listb, merge_dict=True):
    if not lista and listb:
        return listb
    elif not listb and lista:
        return lista
    elif lista:
        tmplist=[]
        if merge_dict:
            tmpdict={}
            for element in lista:
                if type(element) is dict:
                    tmpdict.update(element)
                else:
                    tmpdict.update({element:None})
            for element in listb:
                if type(element) is dict:
                    tmpdict.update(element)
                else:
                    tmpdict.update({element:None})
            for k,v in tmpdict.iteritems():
                if v is None:
                    tmplist.append(k)
                else:
                    tmplist.append({k:v})
        else:
            for element in lista:
                if element not in listb:
                    tmplist.append(element)
            tmplist.extend(listb)
        return tmplist
    else:
        return []

def get_list(myhost, setting, **kwargs):
    default=kwargs.get('default','all')
    merge_list=kwargs.get('merge_list',False)
    merge_dict=kwargs.get('merge_dict',True)
    check_osver=kwargs.get('check_osver',False)
    context={}
    root_value=setting
    # get default
    context['default']=[]
    if check_osver:
        if not context['default']:
            # key:
            #   default:
            #     os_ver:
            context['default'].extend(root_value.get('default',{}).get(myhost['os_ver'],[]))
            # key:
            #   default:
            #     subos_ver:
            context['default']=join_list(context['default'],root_value.get('default',{}).get(myhost['os_subver'],[]),merge_dict)
        if not context['default']:
            # key:
            #   default:
            #     default_os:
            context['default'].extend(root_value.get('default',{}).get('default_os',[]))
    else:
        # key:
        #   default:
        context['default'].extend(root_value.get('default',[]))
    if default == 'all':
        for attr in SETTING_LIST:
            context[attr]=get_host_list(myhost, root_value, attr, kwargs)
            context['default'] = join_list(context['default'], context[attr],merge_dict)
        return context['default']
    else:
        for attr in reversed(SETTING_LIST):
            context[attr]=get_host_list(myhost, root_value, attr, kwargs)
            if context[attr]:
                return context[attr]
        return context['default']
