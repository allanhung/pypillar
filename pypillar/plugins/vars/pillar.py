# (c) 2013, Paralect <info@paralect.com>
#
# ansible-pillar-plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ansible-pillar-plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ansible-pillar-plugin.  If not, see <http://www.gnu.org/licenses/>.


import os
import glob
from ansible import errors
from ansible.utils import vars
from ansible.parsing.dataloader import DataLoader
import ansible.constants as C

class VarsModule(object):
    
    """
    Loads variables from 'pillar/' directory in inventory base directory or in the same directory
    as the playbook. If inventory base directory and playbook base directory both contain 'pillar/'
    directory, then only 'pillar/' in playbook directory will be used.
    
    You can explicitly specify ANSIBLE_PILLARS_DIRECTORY environment variable. In this case it will 
    take precedence, and 'pillar/' folders in inventory base directory and playbook base directory
    will not be scanned at all.
    """

    def __init__(self, inventory):

        """ constructor """

        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()
        self.loader = DataLoader()
        basedir = inventory.playbook_basedir()
        if basedir is not None: 
            basedir = os.path.abspath(basedir)
        self.playbook_basedir = basedir
        
        
    def get_pillar_path(self):
        
        """
        Returns absolute path to the 'pillar/' folder or None, if it cannot be calculated.
        """
        
        # First try to use ANSIBLE_PILLARS_DIRECTORY environment variable
        # Use this path, if it exists and not empty
        env_ansible_pillar_path = os.environ.get('ANSIBLE_PILLARS_DIRECTORY')
        if env_ansible_pillar_path is not None and env_ansible_pillar_path != "":
            
            pillar_path = os.path.abspath(env_ansible_pillar_path)
            
            # In case there is no such directory, stop
            if (not os.path.exists(pillar_path) or 
                not os.path.isdir(pillar_path)):
                raise errors.AnsibleError("Profiles directory that is specified by ANSIBLE_PILLARS_DIRECTORY does not exists or not a directory: %s" % env_ansible_pillar_path)
            
            return pillar_path
        
        # Second, try to use 'pillar/' directory in playbook directory.
        # If not found, then use 'pillar/' in inventory directory.
        for basedir in [ self.playbook_basedir, self.inventory_basedir ]:
            if basedir is None:
                continue
            
            pillar_path = os.path.abspath(os.path.join(basedir, "pillar"))
            
            if (not os.path.exists(pillar_path) or
                not os.path.isdir(pillar_path)):
                continue
            
            return pillar_path
            
        # It means that we didn't find path to 'pillar/' directory
        return None
        
        
    def get_config(self):
        
        """
        Returns config dictionary or None, if config cannot be constructed.
        """        
        config = {}
        
        # First, try to use ANSIBLE_PILLAR environment variable
        # Use this variable if it exists
        env_ansible_pillar = os.environ.get('ANSIBLE_PILLAR')
        if env_ansible_pillar is not None:
            config['pillar'] = env_ansible_pillar
            
        # Second, try to use '.pillar' file in playbook directory.
        # If not found, then use '.pillar' in inventory directory.
        else: 
            for basedir in [ self.playbook_basedir, self.inventory_basedir ]:
                
                if basedir is None:
                    continue
                
                config_path = os.path.abspath(os.path.join(basedir, ".pillar"))
                
                # If there is no such file, proceed to the next folder
                if (not os.path.exists(config_path) or
                    not os.path.isfile(config_path)):
                    continue
                
                data = self.loader.load_from_file(config_path)
                if type(data) != dict:
                    raise errors.AnsibleError("%s must be stored as a dictionary/hash" % path)

                config = data
        
        return self.sanitize_config(config)

    
    def sanitize_config(self, config):
    
        if 'pillar' not in config or config['pillar'] is None:
            config['pillar'] = ''
            
        # Remove leading '/' symbol
        # We do not support absolute paths for now
        if config['pillar'].startswith('/'):
            config['pillar'] = config['pillar'][1:]
    
        return config
        

    def run(self, host, vault_password):

        """ Main body of the plugin, does actual loading """

        results = {}

        # Load config
        config = self.get_config()
        if config is None:
            return results

        # Calculate pillar path (path to the 'pillar/' directory)
        pillar_path = self.get_pillar_path()
        
        # Prepare absolute pillar path (path to the actual pillar folder
        # in 'pillar/' folder)
        pillar_path = os.path.join(pillar_path, config['pillar']) if config['pillar'] else pillar_path
        if not os.path.exists(pillar_path) or not os.path.isdir(pillar_path):
            raise errors.AnsibleError("There is no such pillar: %s" % pillar_path)            
        
        # Start from specified pillar path
        current_path = os.path.abspath(pillar_path)
        
        # Traverse directories up, until we reach 'pillar_path'
        while True:
            files = [os.path.join(current_path,x) for x in os.listdir(current_path) if os.path.isfile(os.path.join(current_path,x))]
            for vars_path in files:
#                vars_path = os.path.join(current_path, "vars.yml")
            
                if (os.path.exists(vars_path) and 
                    os.path.isfile(vars_path) and
                    os.stat(vars_path).st_size != 0):            
            
                    data = self.loader.load_from_file(vars_path)
#                    if type(data) != dict:
#                        raise errors.AnsibleError("%s must be stored as a dictionary/hash" % vars_path)            
                 
                    results = vars.combine_vars(data, results)
            # if we reached pillar folder, than we traversed all 
            # directories till pillar folder.
            if current_path == pillar_path:
                break;
            
            # select parent directory
            current_path = os.path.abspath(os.path.join(current_path, os.pardir))
 
        # debug
        #print(results)            
        # all done, results is a dictionary of variables
        return results


