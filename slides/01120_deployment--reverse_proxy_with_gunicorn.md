Deploying Flask
===============

1. Set up reverse proxy with your choice of web server
2. Start Flask application with `Gunicorn`

<!--  -->
	#!apache
	<VirtualHost *:80>
	        ServerName example.com

	        ProxyPass / http://127.0.0.1:8000/
	        ProxyPassReverse / http://127.0.0.1:8000/
	</VirtualHost>

<!--  -->

	#!bash
	gunicorn --bind 127.0.0.1:8000 app:app
