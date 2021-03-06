from fabric.api import local
from fabric.api import task
import os
import grp
import pwd

PROJECT_ROOT = os.path.dirname(__file__)
SUPPORT_CONFIG_PROJECT = ['git', 'ack', 'octave', 'eslint', 'atom', 'vscode']
SUPPORT_INSTALL_PROJECT = ['npm', 'atom', 'vscode']


def _get_directory_username_and_groupname(directory):
    statInfo = os.stat(directory)
    uid = statInfo.st_uid
    gid = statInfo.st_gid
    user = pwd.getpwuid(uid)[0]
    group = grp.getgrgid(gid)[0]
    return user, group


def config_template(srcDirectory, destDirectory, files, force=False):
    """Template for config_* tasks

    Parameters:

    - `srcDirectory`: Path of source directory relative to the PROJECT_ROOT
    - `destDirectory`: Full path of destination directory
    - `files`: Array of filenames which will be copied
    - `force`: Boolean whether we should override exisiting files

    Return:

    - None
    """
    # Figure out the full path
    srcDir = os.path.join(PROJECT_ROOT, srcDirectory)
    srcDir = os.path.abspath(srcDir)
    dstDir = os.path.expanduser(destDirectory)
    dstDir = os.path.abspath(dstDir)

    user, group = _get_directory_username_and_groupname(dstDir)

    print '> COPY CONFIGURATION'
    for f in files:
        cmd = 'ln %s -s %s/%s %s/.%s' % (
            '-f' if force else '',
            srcDir,
            f,
            dstDir,
            f
        )
        local(cmd)
        cmd = 'chown -h %s:%s %s/.%s' % (user, group, dstDir, f)
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


def config_atom():
    """Config atom
    """
    files = ['config.cson', 'keymap.cson', 'snippets.cson']

    config_template('atom', '~', files, True)


def config_vscode():
    """Config vscode
    """
    srcDir = os.path.join(PROJECT_ROOT, 'vscode')
    srcDir = os.path.abspath(srcDir)
    dstDir = os.path.expanduser('~')
    dstDir = os.path.abspath(dstDir)
    dstFile = '%s/.config/Code/User/settings.json' % dstDir

    cmd = 'ln -f -s %s/settings.json %s' % (srcDir, dstFile)
    local(cmd)

    user, group = _get_directory_username_and_groupname(dstDir)
    cmd = 'chown -h %s:%s %s' % (user, group, dstFile)
    local(cmd)


def install_npm():
    """Install npm and install pacakges which required npm
    """
    print '> CHECK NPM INSTALLATION'
    local('which npm')

    print '> INSTALL PACKAGES VIA NPM'
    cmd = 'sh %s/npm/install.sh' % PROJECT_ROOT
    local(cmd)


def install_atom():
    """Install atom and install packages which required apm
    """
    print '> CHECK APM INSTALLATION'
    local('which apm')

    print '> INSTALL PACKAGES VIA APM'
    cmd = 'sudo -H -u %s apm stars --user mondwan --install' % (
        os.environ['SUDO_USER']
    )
    local(cmd)


def install_vscode():
    """Install vscode and install pacakges which required vscode
    """
    print '> CHECK vscode INSTALLATION'
    local('which code')

    print '> INSTALL PACKAGES VIA vscode'
    cmd = 'sh %s/vscode/install.sh' % PROJECT_ROOT
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
    elif project == 'atom':
        config_atom()
     elif project == 'vscode':
        config_vscode()


@task
def install(project):
    """Run installation script for given project if possible
    """
    assert project in SUPPORT_INSTALL_PROJECT

    print '> CHECK ROOT PRIVILEGES'
    assert os.getuid() == 0

    if project == 'npm':
        install_npm()
    elif project == 'atom':
        install_atom()
    elif project == 'vscode':
        install_vscode()


@task
def make():
    """Install and config in one command
    """
    for pkg in SUPPORT_INSTALL_PROJECT:
        install(pkg)

    for pkg in SUPPORT_CONFIG_PROJECT:
        config(pkg)
