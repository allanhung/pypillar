#!/usr/bin/python

def parser_host(hostname, osdistribution, osver):
    """
    set host attr by os version, hostname

    os_ver: 
      Microsoft Windows Server 2012 R2 Standard: 6.3.9600.0

    """
    results = {}
    host, domain = hostname.split('.',1)
    os_ver_list = osver.split('.')
    if 'windows' in osdistribution.lower():
        results['os_ver'] = os_ver_list[0]+'.'+os_ver_list[1]
        results['os_subver'] = os_ver_list[2]+'.'+os_ver_list[3]
        results['distribution'] = 'windows'
    elif 'centos' in osdistribution.lower():
        results['os_ver'] = os_ver_list[0]
        results['os_subver'] = os_ver_list[0]+'.'+os_ver_list[1]
        results['distribution'] = 'linux'
    else:
        results['os_ver'] = os_ver_list[0]
        results['os_subver'] = os_ver_list[0]+'.'+os_ver_list[1]
        results['distribution'] = 'linux'
    results['os_ver'] = eval(results['os_ver'])
    results['os_subver'] = eval(results['os_subver'])
    results['hostname'] = host.lower()
    results['domain'] = domain.lower()
    return results
