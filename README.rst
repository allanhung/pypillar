******************
What is pypillar?
******************

Pypillar is an variable setting style like saltslack pillar.


==================
Configuration
==================

Configuration for module::
    export pypillar_location=$(python -c "import os,pypillar; print(os.path.dirname(pypillar.__file__))")
    cat > ansible.cfg <<EOF
    [defaults]
    # vars_plugins configuration is required for the pypillar
    vars_plugins = $pypillar_location/plugins/vars
    # using ":" to spearate multi path
    library = $pypillar_location/plugins/modules
    EOF
