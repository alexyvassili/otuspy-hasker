"""
    This is fabfile for deploying hasker on debian stretch on custom python 3.6.5
    You can manually install python3.6 to /usr/local/bin e.g. from Anaconda distribution
    So, the you need run
    $ sudo apt-get install uwsgi uwsgi-src uuid-dev libcap-dev libpcre3-dev
    $ export PYTHON=python3.6
    $ uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python36"
    $ sudo mv python36_plugin.so /usr/lib/uwsgi/plugins/python36_plugin.so
    $ sudo chmod 644 /usr/lib/uwsgi/plugins/python36_plugin.so
    (see http://www.paulox.net/2017/04/04/how-to-use-uwsgi-with-python3-6-in-ubuntu/)
    if you hav an error about recompile with -fPIC flag - just remove your python3.6:
    this script will install and compile python3.6 and wsgi plugin automatically
"""
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
    input('setenv')
    set_env()
    run('uname -a')
    input('prepare_package_system')
    prepare_package_system()
    input('prepare_interpreter')
    prepare_interpreter()
    input('prepare_uwsgi')
    prepare_uwsgi()
    input('install_system_libs')
    install_system_libs()
    input('create_folders')
    create_folders()
    input('get_src')
    get_src()
    input('set_secrets')
    set_secrets()
    input('create_virtualenv')
    create_virtualenv()
    input('install_venv_libs')
    install_venv_libs()
    input('configure_postgresql')
    configure_postgresql()
    input('configure_nginx')
    configure_nginx()
    input('configure_uwsgi')
    configure_uwsgi()
    input('run_django_postbootstrap_commands')
    run_django_postbootstrap_commands()
    input('restart_all')
    restart_all()


def set_env():
    env.USER = 'alexey'
    env.BASE_PATH = '/var/www'
    env.VENV_PATH = '/var/pyvenvs'
    env.PROJECT_NAME = 'hasker'
    env.PROJECT_DATABASE = 'hasker_db'
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
            run('tar xvf /tmp/Python-3.6.5.tgz -C /tmp/')
            cd('/tmp/Python-3.6.5')
            run('cd /tmp/Python-3.6.5; /tmp/Python-3.6.5/configure --enable-shared --enable-optimizations --with-ensurepip=install')
            run('cd /tmp/Python-3.6.5; make -j8')
            sudo('cd /tmp/Python-3.6.5; make altinstall')
        elif need_compile.lower() == 'n':
            print('OK, exiting')
            sys.exit(1)
        else:
            prepare_interpreter()


def prepare_uwsgi():
    pass
    # sudo('aptitude install python3 python-dev python3-dev uwsgi uwsgi-src uuid-dev libcap-dev libpcre3-dev')
    # run('export PYTHON=python3.6')
    # if not exists('/usr/lib/uwsgi/plugins/python36_plugin.so'):
    #     run('uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python36"')
    #     sudo('mv python36_plugin.so /usr/lib/uwsgi/plugins/python36_plugin.so')
    #     sudo('chmod 644 /usr/lib/uwsgi/plugins/python36_plugin.so')


    # you can verify correct uwsgi and django installation by command
    # (after run django postinstall commands)
    # $ source /var/pyvenvs/hasker/bin/activate
    # $ python manage.py runserver
    # and if it's run ok, then
    # uwsgi --plugins http,python36 --http :8080 --virtualenv /var/pyvenvs/hasker/ \
    # --chdir /var/www/hasker/ -w hasker.wsgi
    sudo('/usr/local/bin/pip3.6 install uwsgi')


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
            'DB_NAME': env.PROJECT_DATABASE,
        },
        use_jinja=True
    )
    sudo('systemctl start postgresql')
    # Create db_user if not exists
    run(f"sudo -u postgres psql -tc \"SELECT 1 FROM pg_catalog.pg_roles WHERE rolname = '{DB_USER}'\" | "
        f"grep -q 1 || sudo -u postgres psql -c \"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}'\"")
    run(f'cd {env.REMOTE_PROJECT_PATH}; sudo -u postgres psql -f fabdeploy/setup_db.sql')
    # Create database if not exists
    run(f"sudo -u postgres psql -tc \"SELECT 1 FROM pg_database WHERE datname = '{env.PROJECT_DATABASE}'\" | "
        f"grep -q 1 || sudo -u postgres psql -c \"CREATE DATABASE {env.PROJECT_DATABASE} OWNER {DB_USER}\"")


def configure_nginx():
    sudo('cp /var/www/hasker/fabdeploy/hasker_nginx /etc/nginx/sites-available/hasker')
    sites_enabled_link = os.path.join(
        '/etc/nginx/sites-enabled',
        env.PROJECT_NAME,
    )
    if not exists(sites_enabled_link):
        available_link_path = os.path.join('/etc/nginx/sites-available', env.PROJECT_NAME)
        sudo(f'ln -s {available_link_path} {sites_enabled_link}')


def configure_uwsgi():
    sudo('mkdir -p /etc/uwsgi/sites')
    sudo('cp /var/www/hasker/fabdeploy/hasker.ini /etc/uwsgi/sites/')
    sudo('cp /var/www/hasker/fabdeploy/uwsgi.service /etc/systemd/system/')
    sudo('systemctl enable nginx')
    sudo('systemctl enable uwsgi')


def run_django_postbootstrap_commands():
    _run_django_management_command('migrate')
    _run_django_management_command('collectstatic --noinput')


def restart_all():
    sudo('systemctl restart nginx')
    sudo('systemctl restart uwsgi')


def _mkdir(path: str, use_sudo=False, chown=False):
    if use_sudo:
        sudo(f'mkdir -p {path}')
        if chown:
            sudo(f'chown {env.USER} {path}')
    else:
        run('mkdir -p %s' % path)


def _put_template(template_name, remote_path, use_sudo=False):
    upload_template(
        os.path.join('fabdeploy', template_name),
        remote_path,
        context={
            'app_name': env.PROJECT_NAME,
        },
        use_sudo=use_sudo,
    )


def _run_django_management_command(command):
    # run('DJANGO_CONFIGURATION=%s %s %s %s' % (
    #     env.DJANGO_CONFIGURATION,
    #     env.VENV_REMOTE_PYTHON_PATH,
    #     os.path.join(env.REMOTE_PROJECT_PATH, 'manage.py'),
    #     command,
    # ))
    # just e.g. python manage.py migrate
    run(f"{env.VENV_REMOTE_PYTHON_PATH} {os.path.join(env.REMOTE_PROJECT_PATH, 'manage.py')} {command}")
