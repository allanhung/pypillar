What is pypillar?
=========================

Pypillar is an variable setting style like saltslack pillar.

Configuration
=========

::

    export pypillar_location=$(python -c "import os,pypillar; print(os.path.dirname(pypillar.__file__))")

    cat > ansible.cfg <<EOF
    [defaults]
    # vars_plugins configuration is required for the pypillar
    action_plugins = $pypillar_location/plugins/actions
    vars_plugins = $pypillar_location/plugins/vars
    # using ":" to spearate multi path
    library = $pypillar_location/modules
    EOF

    # test
    ansible-playbook -i host site.yml
