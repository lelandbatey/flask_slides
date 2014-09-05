Templating
==========

- Pass in variables
- Conditionals within the template

<!--  -->

	::jinja2 hl_lines="2 3"
	<!doctype html>
	{% if name %}
	  <h1>Hello {{ name }}!</h1>
	{% else %}
	  <h1>Hello World!</h1>
	{% endif %}
	</html>

<!--  -->

	::python hl_lines="3"
	@app.route('/hello')
	def root(var):
		return render_template('hello.html', name="PNNL")