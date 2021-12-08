from fabric.tasks import task
from invoke import Collection
import os
import grp
import pwd
import sys


PROJECT_ROOT = os.path.dirname(__file__)
SUPPORT_CONFIG_PROJECT = ['git', 'ack', 'octave', 'eslint', 'atom', 'vscode']
SUPPORT_INSTALL_PROJECT = ['npm', 'atom', 'vscode']


def _get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    sysBasePrefix = getattr(sys, 'base_prefix', None)
    sysRealPrefix = getattr(sys, 'real_prefix', None)
    sysPrefix = sys.prefix
    return sysBasePrefix or sysRealPrefix or sysPrefix

def _in_virtualenv():
    return _get_base_prefix_compat() != sys.prefix


def _run(c, cmd):
    inVirtualEnv = _in_virtualenv()
    if not inVirtualEnv:
        raise Exception('Not under virtualenv')

    return c.run(cmd, replace_env=False, echo=True)


def _get_directory_username_and_groupname(directory):
    statInfo = os.stat(directory)
    uid = statInfo.st_uid
    gid = statInfo.st_gid
    user = pwd.getpwuid(uid)[0]
    group = grp.getgrgid(gid)[0]
    return user, group


def config_template(c, srcDirectory, destDirectory, files, force=False):
    """Template for config_* tasks

    Parameters:

    - `c`: The fabric context
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

    print('> COPY CONFIGURATION')
    for f in files:
        cmd = 'ln %s -s %s/%s %s/.%s' % (
            '-f' if force else '',
            srcDir,
            f,
            dstDir,
            f
        )
        _run(c, cmd)
        cmd = 'chown -h %s:%s %s/.%s' % (user, group, dstDir, f)
        _run(c, cmd)


def config_git(c):
    """Config git project
    """
    files = ['gitconfig', 'gitignore']

    print('> CHECK GIT INSTALLATION')
    _run(c, 'which git')

    config_template(c, 'git', '~', files)


def config_ack(c):
    """Config ack grep
    """
    files = ['ackrc']

    print('> CHECK ACK INSTALLATION')
    _run(c, 'which ack || which ack-grep')

    config_template(c, 'ack', '~', files)


def config_octave(c):
    """Config octave
    """
    files = ['octaverc']

    config_template(c, 'octave', '~', files)


def config_eslint(c):
    """Config eslint
    """
    files = ['eslintrc.json']

    config_template(c, 'eslint', '~', files)


def config_atom(c):
    """Config atom
    """
    files = ['config.cson', 'keymap.cson', 'snippets.cson']

    config_template(c, 'atom', '~', files, True)


def config_vscode(c):
    """Config vscode
    """
    srcDir = os.path.join(PROJECT_ROOT, 'vscode')
    srcDir = os.path.abspath(srcDir)
    dstDir = os.path.expanduser('~')
    dstDir = os.path.abspath(dstDir)
    dstFile = '%s/.config/Code/User/settings.json' % dstDir

    cmd = 'ln -f -s %s/settings.json %s' % (srcDir, dstFile)
    _run(c, cmd)

    user, group = _get_directory_username_and_groupname(dstDir)
    cmd = 'chown -h %s:%s %s' % (user, group, dstFile)
    _run(c, cmd)


def install_npm(c):
    """Install npm and install pacakges which required npm
    """
    print('> CHECK NPM INSTALLATION')
    _run(c, 'which npm')

    print('> INSTALL PACKAGES VIA NPM')
    cmd = 'sh %s/npm/install.sh' % PROJECT_ROOT
    _run(c, cmd)


def install_atom(c):
    """Install atom and install packages which required apm
    """
    print('> CHECK APM INSTALLATION')
    _run(c, 'which apm')

    print('> INSTALL PACKAGES VIA APM')
    cmd = 'sudo -H -u %s apm stars --user mondwan --install' % (
        os.environ['SUDO_USER']
    )
    _run(c, cmd)


def install_vscode(c):
    """Install vscode and install pacakges which required vscode
    """
    print('> CHECK vscode INSTALLATION')
    _run(c, 'which code')

    print('> INSTALL PACKAGES VIA vscode')
    cmd = 'sh %s/vscode/install.sh' % PROJECT_ROOT
    _run(c, cmd)


@task
def config(c, project):
    """Run configuration script for given project if possible
    """
    assert project in SUPPORT_CONFIG_PROJECT

    if project == 'git':
        config_git(c)
    elif project == 'ack':
        config_ack(c)
    elif project == 'octave':
        config_octave(c)
    elif project == 'eslint':
        config_eslint(c)
    elif project == 'atom':
        config_atom(c)
    elif project == 'vscode':
        config_vscode(c)


@task
def install(c, project):
    """Run installation script for given project if possible
    """
    assert project in SUPPORT_INSTALL_PROJECT

    print('> CHECK ROOT PRIVILEGES')
    assert os.getuid() == 0

    if project == 'npm':
        install_npm(c)
    elif project == 'atom':
        install_atom(c)
    elif project == 'vscode':
        install_vscode(c)


@task
def make(c):
    """Install and config in one command
    """
    for pkg in SUPPORT_INSTALL_PROJECT:
        install(c, pkg)

    for pkg in SUPPORT_CONFIG_PROJECT:
        config(c, pkg)


ns = Collection()
ns.add_task(config)
ns.add_task(make)
ns.add_task(install)
