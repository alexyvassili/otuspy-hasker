import os
import sys

from fabric.state import env
from fabric.api import cd, run, sudo, settings
from fabric.contrib.files import exists, upload_template

from hasker.secrets import DB_PASSWORD, DB_USER


USER = 'alexey'
HOST = 'alexyvassili.me'

env.hosts = ['alexey@192.168.0.138']


def bootstrap():
    set_env()
    run('uname -a')
    # prepare_package_system()
    # prepare_interpreter()
    # install_system_libs()
    # create_folders()
    # get_src()
    # set_secrets()
    # create_virtualenv()
    # install_venv_libs()
    configure_postgresql()
    # configure_nginx()
    # configure_uwsgi()
    # run_django_postbootstrap_commands()
    # restart_all()


def set_env():
    env.USER = 'alexey'
    env.BASE_PATH = '/var/www'
    env.VENV_PATH = '/var/pyvenvs'
    env.PROJECT_NAME = 'hasker'
    env.REMOTE_PROJECT_PATH = os.path.join(env.BASE_PATH, env.PROJECT_NAME)
    env.REMOTE_VENV_PATH = os.path.join(env.VENV_PATH,
                                        env.PROJECT_NAME)
    env.GIT_REPO_PATH = "https://github.com/alexyvassili/otuspy-hasker.git"
    if exists('/usr/bin/python3.6'):
        env.BASE_REMOTE_PYTHON_PATH = '/usr/bin/python3.6'
    else:
        env.BASE_REMOTE_PYTHON_PATH = '/usr/local/bin/python3.6'
    env.VENV_REMOTE_PYTHON_PATH = os.path.join(env.REMOTE_VENV_PATH, 'bin', 'python3.6')


def prepare_package_system():
    if not exists('/etc/apt/sources.list.old'):
        sudo('mv /etc/apt/sources.list /etc/apt/sources.list.old')
        upload_template('fabdeploy/sources.list', '/etc/apt/',use_sudo=True)
    sudo('apt-get update && apt-get upgrade')
    sudo('apt-get install -y aptitude')
    sudo('aptitude install -y mc vim')


def prepare_interpreter():
    if not exists(env.BASE_REMOTE_PYTHON_PATH):
        need_compile = input("""Python 3.6 interpreter not found.
                             Do you want download and compile this? (y/n) """)
        if need_compile.lower() == 'y':
            sudo('apt-get install -y make build-essential libssl-dev zlib1g-dev')
            sudo('apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm')
            sudo('apt-get install -y libncurses5-dev libncursesw5-dev xz-utils tk-dev')
            if exists('/tmp/Python-3.6.5.tgz'):
                run('rm /tmp/Python-3.6.5.tgz')
            run('wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz -O /tmp/Python-3.6.5.tgz')
            run('tar xvf Python-3.6.5.tgz -C /tmp/')
            cd('/tmp/Python-3.6.5')
            run('cd /tmp/Python-3.6.5; /tmp/Python-3.6.5/configure --enable-optimizations --with-ensurepip=install')
            run('cd /tmp/Python-3.6.5; make -j8')
            sudo('cd /tmp/Python-3.6.5; make altinstall')
        elif need_compile.lower() == 'n':
            print('OK, exiting')
            sys.exit(1)
        else:
            prepare_interpreter()


def install_system_libs():
    sudo('aptitude install -y postgresql nginx git')


def create_folders():
    _mkdir(env.REMOTE_PROJECT_PATH, use_sudo=True, chown=True)
    _mkdir(env.REMOTE_VENV_PATH, use_sudo=True, chown=True)


def get_src():
    if not exists(os.path.join(env.REMOTE_PROJECT_PATH, '.git')):
        run(f'git clone {env.GIT_REPO_PATH} {env.REMOTE_PROJECT_PATH}')
    else:
        run(f'cd {env.REMOTE_PROJECT_PATH}; git pull')


def set_secrets():
    upload_template(
        os.path.join(env.PROJECT_NAME, 'secrets.py'),
        os.path.join(env.REMOTE_PROJECT_PATH, env.PROJECT_NAME)
    )


def create_virtualenv():
    if not exists(env.VENV_REMOTE_PYTHON_PATH):
        run(f'{env.BASE_REMOTE_PYTHON_PATH} -m venv {env.REMOTE_VENV_PATH}')
        pip = os.path.join(env.REMOTE_VENV_PATH, 'bin', 'pip3')
        run(f'{pip} install --upgrade pip')


def install_venv_libs():
    requirements_txt = os.path.join(env.REMOTE_PROJECT_PATH, 'requirements.txt')
    run(f'{env.VENV_REMOTE_PYTHON_PATH} -m pip install -r {requirements_txt}')


def configure_postgresql():
    upload_template(
        os.path.join('fabdeploy', 'setup_db.sql'),
        os.path.join(env.REMOTE_PROJECT_PATH, 'fabdeploy'),
        context={
            'DB_USER': DB_USER,
            'DB_PASSWORD': DB_PASSWORD,
        }
    )
    # sudo('systemctl start postgresql')
    # cd(env.REMOTE_PROJECT_PATH)
    # run(f'sudo -u postgres psql -f fabdeploy/setup_db.sql -v user={DB_USER} -v pwd={DB_PASSWORD}')


def configure_nginx():
    _put_template(
        'nginx.conf',
        os.path.join('/etc/nginx/sites-available', env.PROJECT_NAME)
    )
    sites_enabled_link = os.path.join(
        '/etc/nginx/sites-enabled',
        env.PROJECT_NAME,
    )
    if not exists(sites_enabled_link):
        available_link_path = os.path.join('/etc/nginx/sites-available', env.PROJECT_NAME)
        sudo(f'ln -ls {available_link_path} {sites_enabled_link}')


def configure_uwsgi():
    pass


def run_django_postbootstrap_commands():
    _run_django_management_command('migrate')
    _run_django_management_command('collectstaic --noinput')


def restart_all():
    sudo('systemctl restart nginx')
    run('systemctl restart uwsgi')


def _mkdir(path: str, use_sudo=False, chown=False):
    if use_sudo:
        sudo(f'mkdir -p {path}')
        if chown:
            sudo(f'chown {env.USER} {path}')
    else:
        run('mkdir -p %s' % path)


def _put_template(template_name, remote_path, use_sudo=False):
    upload_template(
        os.path.join('fab_deploy', template_name),
        remote_path,
        context={
            'app_name': env.PROJECT_NAME,
        },
        use_sudo=use_sudo,
    )


def _run_django_management_command(command):
    run('DJANGO_CONFIGURATION=%s %s %s %s' % (
        env.DJANGO_CONFIGURATION,
        env.VENV_REMOTE_PYTHON_PATH,
        os.path.join(env.REMOTE_PROJECT_PATH, 'manage.py'),
        command,
    ))
