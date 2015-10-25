def config_app(app):
	app.config['MYSQL_USER'] = 'root'
	app.config['MYSQL_PASSWORD'] = 'DHGLYjoe521'
	app.config['MYSQL_DB'] = 'group88'
	app.config['MYSQL_HOST'] = 'localhost'
	app.config['MAIL_SERVER'] = 'smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USE_SSL'] = True
	app.config['MAIL_USERNAME'] = 'group88eecs485'
	app.config['MAIL_PASSWORD'] = 'awesomejph'
	app.config['MAIL_DEFAULT_SENDER'] = 'group88eecs485@gmail.com'
