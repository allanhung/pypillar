# (c) 2017, Hung, Allan <hung.allan@gmail.com>
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
from ansible import errors
from ansible.utils import vars
from ansible.plugins.vars import BaseVarsPlugin
from ansible.parsing.dataloader import DataLoader
import ansible.constants as C

class VarsModule(BaseVarsPlugin):
    
    """
    Loads variables from 'pillar/' directory in inventory base directory or in the same directory
    as the playbook. If inventory base directory and playbook base directory both contain 'pillar/'
    directory, then only 'pillar/' in playbook directory will be used.
    
    You can explicitly specify ANSIBLE_PILLARS_DIRECTORY environment variable. In this case it will 
    take precedence, and 'pillar/' folders in inventory base directory and playbook base directory
    will not be scanned at all.
    """

    def get_vars(self, loader, path, entities, cache=True):
        ''' parses the inventory file '''

        super(VarsModule, self).get_vars(loader, path, entities)
        self.inventory_basedir = path
        self.loader = DataLoader()

        results = {}
        # Calculate pillar path (path to the 'pillar/' directory)
        pillar_path = self.get_pillar_path()
        
        # Start from specified pillar path
        cur_path_list = []
        cur_path = os.path.join(os.getcwd(), "pillar")
        if pillar_path == cur_path:
            cur_path = ''
        if cur_path and os.path.exists(cur_path) and os.path.isdir(cur_path):
            cur_path_list.append(os.path.join(cur_path))
        if pillar_path:
            cur_path_list.append(os.path.abspath(pillar_path))
        if not cur_path_list:
            self._display.v('no pillar path found!')
            return results
        # read file with extension '.yml' and folder name not end with '.bak'
        file_list=[]
        for cpath in cur_path_list: 
            self._display.v('Using pillar in path: {}'.format(cpath))
            for root, subdirs, files in os.walk(cpath):
               c_file_list=[]
               if not root.endswith('.bak'):
                   for f in files:
                       if f.endswith('.yml'):
                           c_file_list.append(os.path.join(root,f))
               c_file_list = sorted(c_file_list)
               file_list.extend(c_file_list)
        self._display.vv('loading file list: {}:'.format(file_list))
        for vars_file in reversed(file_list):
            if (os.path.exists(vars_file) and os.path.isfile(vars_file) and os.stat(vars_file).st_size != 0):
                data = self.loader.load_from_file(vars_file)
                results = vars.combine_vars(data, results)

        # debug
        result={'pillar': results}
        self._display.vvv(str(result))
        # all done, results is a dictionary of variables
        return result

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
            if (not os.path.exists(pillar_path) or not os.path.isdir(pillar_path)):
                raise errors.AnsibleError("Profiles directory that is specified by ANSIBLE_PILLARS_DIRECTORY does not exists or not a directory: %s" % env_ansible_pillar_path)            
            self._display.v('Using environment variable ANSIBLE_PILLARS_DIRECTORY: {}'.format(env_ansible_pillar_path))
            return pillar_path
        
        # Second, try to use 'pillar/' directory in playbook directory.
        # If not found, then use 'pillar/' in inventory directory.
        if self.inventory_basedir:
            pillar_path = os.path.abspath(os.path.join(self.inventory_basedir, "pillar"))
        else:    
            return None

        if (not os.path.exists(pillar_path) or not os.path.isdir(pillar_path)):
            self._display.v('pillar path {} not exists!'.format(pillar_path))
            return None
        return pillar_path
