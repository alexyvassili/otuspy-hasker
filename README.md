# otuspy-hasker
A poor-man Stackoverflow based on Django Framework

## Deploy on Ubuntu and Docker
(config in deploy folder)
- ``docker run --rm -it -p 8000:80 /bin/bash  ``
- ``git clone <repo> hasker``
- ``cd hasker``
- ``make prod``

## Deploy on Debian Stretch with fabric
- add your ssh key to `~/.ssh/authorized_keys` on your server
- Check that server name is correct in:
    - `fabfile.py`
    - `fabdeploy/hasker.nginx`
    - `hasker/settings.py`
- Check if virtual environment on your local machine is created with requirements packages
- Just run `fab bootstrap` under virtualev! This command will setup packages, postgres, uwsgi, nginx automatically
- If you want update your site from git repo, run `fab deploy`
- If you want fill your site with test data from toster.ru, run `fab create_demo_data`

#### NOTE:
If `python3.6` not found in `/usr/bin` or in `/usr/local/bin`, `fab bootstrap` will try donwnload precompiled version and
setup it in /usr/local. You can compile interpreter from source with command: `fab compile_interpreter`
In theory you can run with python3.5, just remove before all f-strings from the project :)

## Secrets
And you need your own hasker/secrets.py in your local repository, for example:
```
DB_USER = 'hasker'
DB_PASSWORD = 'hasker_pass'
SECRET_KEY = '14@+4-wet=u8_ns-#ji1)8um5deb*h#'
TEST_USERS_PASS = 'test_password' # password for test users
HASKER_SERVICE_MAIL = 'noreply@hasker.ha'
SUPERUSER = 'admin'
SUPERUSER_PASS = 'admin_pass'
SUPERUSER_MAIL = 'admin@hasker.ha'
```
