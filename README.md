# About

Store configurations for development tools and scripts for setting up a
environment for development as soon as possible.

@author: Mond Wan

@last-modified: 2016-02-29 00:29

# How to run

    # First run: setup repository
    $> mkdir env
    $> virtualenv env/

    # Start running
    $> source env/bin/activate
    $> pip install -r requirement.txt
    $> fab make

# Alternative to config or install

    # Config certain project only
    $> fab config:$CONFIG_PROJECT

    # Install certain project only
    $> fab install:$INSTALL_PROJECT

# List of support $CONFIG_PROJECT $INSTAL_PROJECTL

```python
SUPPORT_CONFIG_PROJECT = ['git', 'ack', 'octave', 'eslint']
SUPPORT_INSTALL_PROJECT = ['npm']
```
