Templating
==========

- Iterate within the template

<!--  -->

	#!jinja2
	<ul>
		{% for slide in list_of_slides %} 		
			<li><a href="/{{ slide }}">{{ slide }}</a></li>
		{% endfor %}
	</ul>
<!--  -->

	::python hl_lines="3 4"
	@app.route('/list')
	def list_slides(var):
		return render_template('list.html',
			list_of_slides=['one','two','three'])