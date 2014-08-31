Routes
======

- Static routes

<!--  -->

	#!python
	@app.route('/present/current_slide')
	def present_current_slide():
		return slide_deck.get_slide_contents(slide_deck.index)

	@app.route('/present/total_slides')
	def total_slides():
		return str(len(slide_deck.get_slide_list()))

	@app.route('/remote/next')
	def next():
		slide.index += 1
		return ""