`Request` and `Response` Objects
================================

- Convenient data accessors for `Request`
	- `get_json` for getting json
	- `data` for getting

<!--  -->


	#!python

	@app.route('/example', methods=['POST'])
	def example_function():
		# The json formatted data (if it's json)
		json_data = request.get_json()
		# The raw data, stored as string
		request_data = request.data