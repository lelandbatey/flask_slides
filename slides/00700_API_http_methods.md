HTTP Methods
============

- By default, a route responds only to `GET`
- Easy to add via `methods` arg of `route` decorator

<!--  -->

	#!python

	@app.route('/login', methods=['GET', 'POST'])
	def login():
	    if request.method == 'POST':
	        do_the_login()
	    else:
	        show_the_login_form()


	



