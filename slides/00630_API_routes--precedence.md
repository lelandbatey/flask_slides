Routes
======

- Prioritizes routes based on "complexity"
	- They work how you'd expect

<!--  -->

	#!python
	@app.route('/foo/<var>')
	def test0(var):
		return "test0: "+var

	@app.route('/<var0>/<var1>')
	def test1(var0, var1):
		return "test1: "+var0+', var: '+var1