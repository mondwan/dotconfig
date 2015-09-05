from fabric.api import local
from fabric.api import task
import os

PROJECT_ROOT = os.path.dirname(__file__)
SUPPORT_CONFIG_PROJECT = ['git']

def config_git():
    """Install git project
    """
    git_dir = os.path.join(PROJECT_ROOT, 'git')
    files = ['gitconfig', 'gitignore']

    print '> CHECK GIT INSTALLATION'
    local('which git')

    print '> SETUP GLOBAL CONFIGURATION'
    for f in files:
        cmd = 'cp %s/%s ~/.%s' % (git_dir, f, f)
        local(cmd)


@task
def config(project):
    """Run configuration script for given project if possible
    """
    assert project in SUPPORT_CONFIG_PROJECT

    if project == 'git':
        config_git()
