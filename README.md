# About

Store configurations for development tools and scripts for setting up a
environment for development as soon as possible.

@author: Mond Wan

@last-modified: 8 DEC 2021

# How to run

    # First run: setup repository with python3
    $> python3 -m venv venv

    # Start running
    $> source venv/bin/activate
    $> pip install -r requirement.txt
    $> fab make

# Alternative to config or install

    # Config certain project only
    $> fab config --project=$CONFIG_PROJECT

    # Install certain project only
    $> fab install --project=$INSTALL_PROJECT

# List of support $CONFIG_PROJECT $INSTAL_PROJECT

```python
SUPPORT_CONFIG_PROJECT = ['git', 'ack', 'octave', 'eslint', 'vscode']
SUPPORT_INSTALL_PROJECT = ['npm', 'atom', 'vscode']
```
