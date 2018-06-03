prod:
	apt-get install sudo

	#python
	apt-get install -y python3
	apt-get install -y python3-pip
	pip3 install --upgrade pip
	pip3 install uwsgi
	pip3 install django==1.11
	pip3 install psycopg2
	pip3 install Pillow

	#postgres
	apt-get install -y postgresql
	apt-get install -y postgresql-server-dev-9.5
	apt-get install -y postgresql-contrib

	#psql настройка
	service postgresql start
	sudo -u postgres psql -f deploy/setup_db.sql -v user=${HASKER_DB_USER} -v pwd=${HASKER_DB_PASSWORD}

	#nginx
	apt-get install -y nginx
	rm /etc/nginx/sites-enabled/default
	cp deploy/hasker_nginx.conf /etc/nginx/conf.d/hasker_nginx.conf
	cp deploy/uwsgi_params uwsgi_params
	/etc/init.d/nginx start

	#django
	python3 manage.py makemigrations
	python3 manage.py migrate

    uwsgi --ini deploy/hasker_uwsgi.ini
