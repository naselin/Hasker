prod:
	echo "Change dumb aliases..."
	alias rm='rm'
	alias cp='cp'
	echo "Done!"

	echo "Settings environment..."
	cp deploy/etc/environment /etc/environment
	echo "Done!"

	echo "Installing RPM's..."
	dnf install -y postgresql-server \
		python2-pip \
		python2-devel \
		python3-pip \
		gcc \
		nginx \
		sudo
	echo "Done!"

	echo "Installing dependencies..."
	ln -s /usr/bin/python2 /usr/bin/python
	pip2 install --upgrade pip
	pip2 install -r deploy/requirments.txt
	echo "Done!"

	echo "Set up database server..."
	sudo -u postgres initdb --no-locale --encoding=UTF8 -D /var/lib/pgsql/data
	sudo -u postgres echo "host    all          hasker          127.0.0.1/32            md5" >> /var/lib/pgsql/data/pg_hba.conf
	sudo -u postgres pg_ctl -D /var/lib/pgsql/data start
	psql -U postgres template1 -f deploy/initial_db.sql
	echo "Done!"

	echo "Set up application..."
	mkdir -p /var/www/hasker
	for line in `cat deploy/appfiles_list.txt`; do cp $$line /var/www/hasker -r; done
	cd /var/www/hasker
	for line in `cat /etc/environment`; do export $$line; done && ./manage.py migrate
	mkdir /tmp/haskermail
	echo "Done!"

	echo "Configuring web-server..."
	cp -f deploy/etc/nginx.conf /etc/nginx/
	nginx
	cp deploy/etc/uwsgi.ini /etc/uwsgi.ini
	mkdir -p /var/run/hasker
	for line in `cat /etc/environment`; do export $$line; done && uwsgi --ini /etc/uwsgi.ini &
	echo "All done!"
