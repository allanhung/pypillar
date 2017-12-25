What is pypillar?
=========================

Pypillar is an variable setting style like saltslack pillar.

How to install
=========================

::

    pip install git+https://github.com/allanhung/pypillar.git

Configuration
=========

::

    export pypillar_location=$(python -c "import os,pypillar; print(os.path.dirname(pypillar.__file__))")

    cat > ansible.cfg <<EOF
    [defaults]
    # action_plugins and vars_plugins configuration is required for the pypillar
    action_plugins = $pypillar_location/plugins/actions
    vars_plugins = $pypillar_location/plugins/vars
    # using ":" to spearate multi path
    library = $pypillar_location/modules
    EOF

    # test
    # modify your host setting in example
    ansible-playbook -i host site.yml

Example
=========

::

    .
    ├── inventory
    │   ├── sub1
    │   │   ├── hosts
    │   │   └── pillar
    │   │       └── stage.yml
    │   └── sub2
    │       ├── hosts
    │       └── pillar
    │           └── stage.yml
    ├── pillar
    │   ├── stage.yml

    ansible-playbook -i inventory/sub1/hosts site.yml
    
This will paser file in pillar first and then paser file in inventory pillar.
If there is same key, key in pillar will replace by key in inventory pillar.
