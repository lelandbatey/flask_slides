<style type="text/css">
pre {
	font-size: 20px;
}

.highlight {
	margin: 0;
	width: auto;
	display: inline-block;
	vertical-align: top;
}

</style>
Routes
======

- Static and Variable routes


<!--  -->
	:::python
	from flask import Flask
	app = Flask(__name__)

	@app.route('/')
	def root():
	    return "This is the default page."

	@app.route('/<some_variable>')
	def vars(some_variable):
	    return "Single variable:\n" + some_variable

	@app.route('/stuff/<var1>/<var2>')
	def multi_vars(var1,var2):
	    return "Var #1: " + var1+"\n Var #2: "+var2

	if __name__ == '__main__':
	    app.run()

<!--  -->

	:::markdown
	Example results when visiting the
	 indicated pages:

	http://host/
		This is the default page


	http://host/quick_brown_fox
		Single variable:
		quick_brown_fox

	http://host/stuff/thing1/other_thing
		Var #1: thing1 
		Var #2: other_thing

	
