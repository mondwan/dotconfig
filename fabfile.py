from fabric.api import local
from fabric.api import task
import os

PROJECT_ROOT = os.path.dirname(__file__)
SUPPORT_CONFIG_PROJECT = ['git', 'ack', 'octave', 'eslint']
SUPPORT_INSTALL_PROJECT = ['npm']


def config_template(srcDirectory, destDirectory, files):
    """Template for config_* tasks

    Parameters:

    - `srcDirectory`: Path of source directory relative to the PROJECT_ROOT
    - `destDirectory`: Full path of destination directory
    - `files`: Array of filenames which will be copied

    Return:

    - None
    """
    # Figure out the full path
    srcDir = os.path.join(PROJECT_ROOT, srcDirectory)

    print '> COPY CONFIGURATION'
    for f in files:
        cmd = 'cp %s/%s %s/.%s' % (srcDir, f, destDirectory, f)
        local(cmd)


def config_git():
    """Config git project
    """
    files = ['gitconfig', 'gitignore']

    print '> CHECK GIT INSTALLATION'
    local('which git')

    config_template('git', '~', files)


def config_ack():
    """Config ack grep
    """
    files = ['ackrc']

    print '> CHECK ACK INSTALLATION'
    local('which ack || which ack-grep')

    config_template('ack', '~', files)


def config_octave():
    """Config octave
    """
    files = ['octaverc']

    config_template('octave', '~', files)


def config_eslint():
    """Config eslint
    """
    files = ['eslintrc.json']

    config_template('eslint', '~', files)


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
    elif project == 'ack':
        config_ack()
    elif project == 'octave':
        config_octave()
    elif project == 'eslint':
        config_eslint()


@task
def install(project):
    """Run installation script for given project if possible
    """
    assert project in SUPPORT_INSTALL_PROJECT

    print '> CHECK ROOT PRIVILEGES'
    assert os.getuid() == 0

    if project == 'npm':
        install_npm()


@task
def make():
    """Install and config in one command
    """
    for pkg in SUPPORT_INSTALL_PROJECT:
        install(pkg)

    for pkg in SUPPORT_CONFIG_PROJECT:
        config(pkg)
