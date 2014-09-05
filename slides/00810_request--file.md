`Request` and `Response` Objects
================================

- `request` file handling from HTML forms

<!--  -->

	#!python
	from flask import request

	@app.route('/upload', methods=['GET', 'POST'])
	def upload_file():
	    if request.method == 'POST':
	        f = request.files['the_file']
	        f.save('/var/www/uploads/uploaded_file.txt')