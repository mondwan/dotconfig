from fabric.api import local
from fabric.api import task
import os

PROJECT_ROOT = os.path.dirname(__file__)
SUPPORT_CONFIG_PROJECT = ['git']
SUPPORT_INSTALL_PROJECT = ['npm']

def config_git():
    """Config git project
    """
    git_dir = os.path.join(PROJECT_ROOT, 'git')
    files = ['gitconfig', 'gitignore']

    print '> CHECK GIT INSTALLATION'
    local('which git')

    print '> SETUP GLOBAL CONFIGURATION'
    for f in files:
        cmd = 'cp %s/%s ~/.%s' % (git_dir, f, f)
        local(cmd)

def install_npm():
    """Install npm and install pacakges which required npm
    """
    print '> CHECK NPM INSTALLATION'
    local('which npm')

    print '> INSTALL PACKAGES VIA NPM'
    cmd = 'sh %s/npm/install.sh' % PROJECT_ROOT
    local(cmd)

@task
def config(project):
    """Run configuration script for given project if possible
    """
    assert project in SUPPORT_CONFIG_PROJECT

    if project == 'git':
        config_git()

@task
def install(project):
    assert project in SUPPORT_INSTALL_PROJECT

    print '> CHECK ROOT PRIVILEGES'
    assert os.getuid() == 0

    if project == 'npm':
        install_npm()
