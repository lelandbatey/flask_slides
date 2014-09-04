Requests
========

- Handling files

<!--  -->

	#!python
	@app.route('/upload', methods=['POST'])
	def upload_file():
		f = request.files['file']
		filename = secure_filename(f.filename)
		f.save(os.path.join(drop_location, filename))
		return redirect(url_for('index'))