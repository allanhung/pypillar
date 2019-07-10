# Pypillar

The purpose of the project is to provide an easy way to setup variable in ansible.

## How to install

```
pip install git+https://github.com/allanhung/pypillar.git
```

## Configuration

The action_plugins and vars_plugins configuration are required for the pypillar, cache plugin is optional.

```
export pypillar_location=$(python -c "import os,pypillar; print(os.path.dirname(pypillar.__file__))")

cat > ansible.cfg <<EOF
[defaults]
gathering=smart
fact_caching=jsonfile_pillar
fact_caching_connection=/tmp/ansible_facts
fact_caching_timeout=7200
action_plugins = $pypillar_location/plugins/actions
cache_plugins = $pypillar_location/plugins/caches
vars_plugins = $pypillar_location/plugins/vars
# using ":" to spearate multi path
library = $pypillar_location/modules
EOF
```

Test if it works.

```
cat > localhost << EOF
[local]  
localhost ansible_connection=local
EOF

mkdir pillar

cat > pillar/vars.yml << EOF
test_message:
  default:
    foo: bar
EOF

cat > pillar_playbook.yml << EOF
- name: pillar test
  hosts: all
  pre_tasks:
    - pillar: {}
  task:
    - debug:
        msg: "{{ pillar.test_message.foo }}"
EOF

# modify your host setting in example
ansible-playbook -i localhost pillar_playbook.yml
```

## How it work

```
 .
 ├── inventory
 │   ├── folder1
 │   │   ├── hosts
 │   │   └── pillar
 │   │       └── vars.yml
 │   └── folder2
 │       ├── hosts
 │       └── pillar
 │           └── vars.yml
 ├── pillar
 │   ├── vars.yml
 
 ansible-playbook -i inventory/folder1/hosts site.yml
```

This will paser file in ./pillar first and then paser file in ./inventory/pillar.
If there are duplicate keys, these keys will replace by key in ./inventory/pillar.
